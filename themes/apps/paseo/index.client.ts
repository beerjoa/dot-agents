// Generated color-only plugin; edit the shared palettes and generator.
import type { PluginClientContext } from "@getpaseo/plugin/client";

export default function contribute(client: PluginClientContext) {
  const themes = [
  {
    "id": "kanagawa-wave",
    "name": "Kanagawa Wave",
    "appearance": "dark",
    "colors": {
      "background": "#1f1f28",
      "foreground": "#dcd7ba",
      "raised": "#17171e",
      "control": "#223249",
      "border": "#54546D",
      "accent": "#7e9cd8",
      "mutedForeground": "#c8c093",
      "ring": "#7e9cd8"
    }
  },
  {
    "id": "kanagawa-lotus",
    "name": "Kanagawa Lotus",
    "appearance": "light",
    "colors": {
      "background": "#f1e9d2",
      "foreground": "#545464",
      "raised": "#e6dcc0",
      "control": "#faf4df",
      "border": "#8a8980",
      "accent": "#4d699b",
      "mutedForeground": "#545464",
      "ring": "#4d699b"
    }
  }
] as const;
  for (const theme of themes) client.addTheme(theme);
  return () => {};
}
