import { root } from "@lynx-js/react";
import { MemoryRouter, Route, Routes } from "react-router";

import { PlantDetail } from "./PlantDetail.jsx";
import { Plants } from "./Plants.jsx";

root.render(
  <MemoryRouter>
    <Routes>
      <Route path="/" element={<Plants />} />
      <Route path="/detail/:species" element={<PlantDetail />} />
    </Routes>
  </MemoryRouter>
);

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept();
}
