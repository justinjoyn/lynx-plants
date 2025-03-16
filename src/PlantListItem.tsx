import "./PlantListItem.css";
import type { Plant } from "./types.js";

export const PlantListItem = ({
  plant,
  onTap,
}: {
  plant: Plant;
  onTap: (plant: Plant) => void;
}) => {
  return (
    <list-item item-key={plant.id} key={plant.id} on-tap={() => onTap(plant)}>
      <view class="plant-list-item">
        <text class="plant-name">{plant.name}</text>
        <text class="plant-species">{plant.species}</text>
        <text class="plant-link">{plant.link}</text>
      </view>
    </list-item>
  );
};
