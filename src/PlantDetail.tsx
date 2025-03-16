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
    <view class="container">
      <text class="title">{plant?.name}</text>
      <text class="description">{plant?.description}</text>
      <text class="species">{plant?.species}</text>
      <text class="link">{plant?.link}</text>
    </view>
  );
};
