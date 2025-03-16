import { useState } from "react";

import { useEffect } from "@lynx-js/react";
import { useNavigate } from "react-router";
import { getPlants } from "./api.js";
import { PlantListItem } from "./PlantListItem.jsx";
import type { Plant } from "./types.js";

export const PlantList = () => {
  const navigate = useNavigate();
  const [plants, setPlants] = useState<Plant[]>([]);

  useEffect(() => {
    getPlants().then((plants) => setPlants(plants));
  }, []);

  const handleTap = (plant: Plant) => {
    navigate(`/detail/${plant.species}`);
  };

  return (
    <list scroll-orientation="vertical" list-type="single" span-count={1}>
      {plants.map((plant, index) => (
        <PlantListItem key={plant.id} plant={plant} onTap={handleTap} />
      ))}
    </list>
  );
};
