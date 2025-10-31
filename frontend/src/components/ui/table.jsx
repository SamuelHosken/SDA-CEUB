import * as React from "react";
export function Table({ className = "w-full text-sm", ...props }) {
  return <table className={className} {...props} />;
}
export function TableHeader(props) {
  return <thead {...props} />;
}
export function TableBody(props) {
  return <tbody {...props} />;
}
export function TableRow({ className = "", ...props }) {
  return <tr className={className} {...props} />;
}
export function TableHead({
  className = "text-left text-white border-b border-zinc-800 py-2",
  ...props
}) {
  return <th className={className} {...props} />;
}
export function TableCell({ className = "py-2", ...props }) {
  return <td className={className} {...props} />;
}
export default Table;