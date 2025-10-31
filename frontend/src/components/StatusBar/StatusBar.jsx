import { useEffect, useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  createColumnHelper,
} from "@tanstack/react-table";
import { chatAPI } from "../../services/api";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { Progress } from "../../components/ui/progress";
import { Button } from "../../components/ui/button";
import { Card } from "../../components/ui/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "../../components/ui/table";
const columnHelper = createColumnHelper();
function StatusBar({ sessionId }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sorting, setSorting] = useState([{ id: "timestamp", desc: true }]);
  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 5000);
    return () => clearInterval(interval);
  }, [sessionId]);
  const loadStatus = async () => {
    try {
      const data = await chatAPI.getStatus(sessionId);
      setStatus(data);
    } catch (error) {
      console.error("Erro ao carregar status:", error);
    } finally {
      setLoading(false);
    }
  };
  const handleReset = async () => {
    if (
      !confirm(
        "Tem certeza que deseja resetar toda sua dieta? Isso apagará todo o histórico."
      )
    ) {
      return;
    }
    try {
      await chatAPI.resetar(sessionId);
      setStatus({
        calorias_consumidas: 0,
        meta_calorias: 2600,
        macros_consumidos: { proteinas: 0, carboidratos: 0, gorduras: 0 },
        refeicoes_hoje: 0,
        refeicoes: [],
      });
    } catch (error) {
      alert(
        `Erro ao resetar: ${error.response?.data?.detail || error.message}`
      );
    }
  };
  const refeicoesData = useMemo(() => {
    if (!status?.refeicoes || !Array.isArray(status.refeicoes)) return [];
    return status.refeicoes.map((ref, idx) => ({
      id: idx,
      descricao: ref.descricao || ref.alimento || "Refeição",
      horario:
        ref.horario || ref.timestamp?.split("T")[1]?.substring(0, 5) || "-",
      calorias: ref.calorias || 0,
      proteinas: ref.macros?.proteina_g || ref.macros?.proteinas || 0,
      carboidratos: ref.macros?.carboidratos_g || ref.macros?.carboidratos || 0,
      gorduras: ref.macros?.gorduras_g || ref.macros?.gorduras || 0,
      timestamp: ref.timestamp || new Date().toISOString(),
    }));
  }, [status?.refeicoes]);
  const columns = useMemo(
    () => [
      columnHelper.accessor("horario", {
        header: "Horário",
        cell: (info) => <span>{info.getValue()}</span>,
      }),
      columnHelper.accessor("descricao", {
        header: "Refeição",
        cell: (info) => (
          <span className="text-zinc-400">{info.getValue()}</span>
        ),
      }),
      columnHelper.accessor("calorias", {
        header: "Calorias",
        cell: (info) => <span>{Math.round(info.getValue())} kcal</span>,
      }),
    ],
    []
  );
  const table = useReactTable({
    data: refeicoesData,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });
  if (loading || !status) {
    return (
      <div className="h-screen bg-black text-white overflow-y-auto p-6">
        <div className="space-y-4">
          <div className="h-14 bg-zinc-900 border border-zinc-800 rounded" />
          <div className="h-28 bg-zinc-900 border border-zinc-800 rounded" />
          <div className="h-52 bg-zinc-900 border border-zinc-800 rounded" />
        </div>
      </div>
    );
  }
  const progress = Math.min(
    (status.calorias_consumidas / status.meta_calorias) * 100,
    100
  );
  const macrosData = [
    {
      name: "Proteínas",
      value: status.macros_consumidos.proteinas,
      target: 165,
    },
    {
      name: "Carboidratos",
      value: status.macros_consumidos.carboidratos,
      target: 280,
    },
    { name: "Gorduras", value: status.macros_consumidos.gorduras, target: 75 },
  ];
  const pieData = macrosData.map((item) => ({
    name: item.name,
    value: item.value,
  }));
  const COLORS = ["#ffffff", "#999999", "#666666"];
  return (
    <div className="h-full bg-black text-white overflow-y-auto p-4 md:p-6">
      <div className="space-y-6 md:space-y-8">
        <div className="text-center">
          <p className="text-lg font-semibold">Status Nutricional</p>
          <p className="text-sm text-zinc-400">
            Acompanhe seu progresso diário
          </p>
        </div>
        <Card className="p-4">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm">Calorias Consumidas</p>
            <p className="text-sm font-semibold">{Math.round(progress)}%</p>
          </div>
          <div className="flex items-baseline gap-2 mb-3">
            <p className="text-2xl font-bold">
              {Math.round(status.calorias_consumidas)}
            </p>
            <p className="text-sm text-zinc-400">
              / {status.meta_calorias} kcal
            </p>
          </div>
          <Progress value={progress} />
          <div className="mt-2 text-xs text-zinc-400">
            {Math.max(0, status.meta_calorias - status.calorias_consumidas)}{" "}
            kcal restantes
          </div>
        </Card>
        <div>
          <p className="text-sm font-semibold mb-3">Macronutrientes</p>
          <div className="grid grid-cols-3 gap-3">
            {macrosData.map((macro, idx) => {
              const percentage = Math.min(
                (macro.value / macro.target) * 100,
                100
              );
              return (
                <div
                  key={idx}
                  className="bg-zinc-950 border border-zinc-800 rounded p-3 text-center"
                >
                  <p className="text-xs text-zinc-400 mb-2">
                    {macro.name.substring(0, 4)}
                  </p>
                  <p className="text-lg font-bold mb-2">
                    {macro.value.toFixed(1)}g
                  </p>
                  <div className="h-1.5 rounded bg-zinc-800 overflow-hidden">
                    <div
                      className="h-full bg-white"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <p className="text-xs text-zinc-400 mt-1">{macro.target}g</p>
                </div>
              );
            })}
          </div>
        </div>
        <Card className="p-4">
          <p className="text-sm font-semibold mb-4">Distribuição de Macros</p>
          <ResponsiveContainer width="100%" height={150}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name.substring(0, 1)}: ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={60}
                fill="#888888"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#111",
                  border: "1px solid #333",
                  color: "#fff",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </Card>
        {refeicoesData.length > 0 && (
          <Card className="p-4">
            <p className="text-sm font-semibold mb-4">Histórico de Refeições</p>
            <div className="max-h-56 overflow-auto">
              <Table>
                <TableHeader>
                  {table.getHeaderGroups().map((headerGroup) => (
                    <TableRow key={headerGroup.id}>
                      {headerGroup.headers.map((header) => (
                        <TableHead key={header.id}>
                          {flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                        </TableHead>
                      ))}
                    </TableRow>
                  ))}
                </TableHeader>
                <TableBody>
                  {table.getRowModel().rows.map((row) => (
                    <TableRow key={row.id} className="border-b border-zinc-800">
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id} className="py-2">
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </Card>
        )}
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold mb-1">
            {status.refeicoes_hoje || refeicoesData.length}
          </p>
          <p className="text-sm text-zinc-400">Refeições registradas hoje</p>
        </Card>
        <hr className="border-zinc-800" />
        <Button
          variant="outline"
          onClick={handleReset}
          className="w-full border-red-600 text-red-400 hover:bg-red-950"
        >
          Resetar Dados
        </Button>
      </div>
    </div>
  );
}
export default StatusBar;