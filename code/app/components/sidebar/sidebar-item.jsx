import Link from "next/link";
import { Button } from "@/components/ui/button";

export function SidebarItem({ name, href, icon, current }) {
  return (
    <Link href={href} className="flex flex-col items-center text-secondary-foreground">
      <Button size="md" variant="ghost" color="secondary" isIconOnly className={current && "bg-secondary/70"}>
        {icon}
      </Button>
      <span className="text-xs">{name}</span>
    </Link>
  );
}
