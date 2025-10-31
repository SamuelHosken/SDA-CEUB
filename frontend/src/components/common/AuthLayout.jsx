import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "../ui/card";
export function AuthLayout({
  title,
  subtitle,
  children,
  footer,
  maxWidth = "sm",
}) {
  const maxWidthClasses = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-lg",
  };
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-4 sm:p-6">
      <Card className={`w-full ${maxWidthClasses[maxWidth]}`}>
        {(title || subtitle) && (
          <CardHeader className="text-center pb-4">
            {title && (
              <CardTitle className="text-xl font-semibold mb-2">
                {title}
              </CardTitle>
            )}
            {subtitle && <p className="text-sm text-zinc-400">{subtitle}</p>}
          </CardHeader>
        )}
        <CardContent className="pb-4">{children}</CardContent>
        {footer && <CardFooter className="pt-0 pb-6">{footer}</CardFooter>}
      </Card>
    </div>
  );
}
export default AuthLayout;