import PrelineScript from "@/components/PrelineScript";
import "@/styles/globals.css";

export const metadata = {
  title: "Cubik",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <PrelineScript />
    </html>
  );
}
