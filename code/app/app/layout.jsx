import PrelineScript from "@/components/PrelineScript";
import { Sidebar } from "@/components/sidebar/sidebar";
import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
import "@/styles/globals.css";

config.autoAddCss = false;

export const metadata = {
  title: "Cubik",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="h-svh bg-gray-50">
        <div className="flex h-full gap-4 p-6">
          <aside className="h-full w-[70px] overflow-y-auto rounded-2xl border border-gray-200 bg-white">
            <Sidebar />
          </aside>
          <main className="flex-1 rounded-2xl border border-gray-200 bg-white">{children}</main>
        </div>
      </body>
      <PrelineScript />
    </html>
  );
}
