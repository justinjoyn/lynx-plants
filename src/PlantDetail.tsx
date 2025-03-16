import { useEffect, useState } from "@lynx-js/react";
import { useParams } from "react-router";
import { getPlantDetails } from "./api.js";
import type { Plant } from "./types.js";

export const PlantDetail = () => {
  const { id } = useParams<{ id: string }>();

  const [plant, setPlant] = useState<Plant | null>(null);

  useEffect(() => {
    if (!id) return;
    getPlantDetails(id).then((plant) => {
      setPlant(plant);
    });
  }, [id]);

  return (
    <view>
      <text>{plant?.name}</text>
      <text>{plant?.description}</text>
      <text>{plant?.species}</text>
      <text>{plant?.link}</text>
    </view>
  );
};
