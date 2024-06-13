"use client";

import { useSelectedLayoutSegment } from "next/navigation";
import { SidebarItem } from "@/components/sidebar/sidebar-item";
import {
  faGear,
  faHouse,
  faRectanglesMixed,
  faRectangleVerticalHistory,
  faRocketLaunch,
  faShuffle,
} from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export function Sidebar() {
  // active route segment, per identificare il link corrente
  const segment = useSelectedLayoutSegment();

  // link della sidebar
  const links = [
    {
      name: "Home",
      href: "/home",
      icon: <FontAwesomeIcon icon={faHouse} size="lg" />,
    },
    {
      name: "Solve",
      href: "/solve",
      icon: <FontAwesomeIcon icon={faRocketLaunch} size="lg" />,
    },
    {
      name: "Scramble",
      href: "/scramble",
      icon: <FontAwesomeIcon icon={faShuffle} size="lg" />,
    },
    {
      name: "Patterns",
      href: "/patterns",
      icon: <FontAwesomeIcon icon={faRectanglesMixed} size="lg" />,
    },
    {
      name: "History",
      href: "/history",
      icon: <FontAwesomeIcon icon={faRectangleVerticalHistory} size="lg" />,
    },
  ];

  return (
    <div className="flex h-full flex-col gap-4 pb-4 pt-4">
      <header className="flex justify-center">
        <a className="text-2xl font-semibold">C</a>
      </header>
      <nav className="flex h-full flex-col gap-2">
        {links.map((link) => (
          <SidebarItem name={link.name} href={link.href} icon={link.icon} current={`/${segment}` === link.href} />
        ))}
        <div className="flex-1"></div>
        <SidebarItem
          name="Settings"
          href="/settings"
          icon={<FontAwesomeIcon icon={faGear} size="lg" />}
          current={`/${segment}` === "/settings"}
        />
      </nav>
    </div>
  );
}
