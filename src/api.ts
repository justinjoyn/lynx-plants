import plants from "./assets/data/plants.json";
import type { Plant } from "./types.js";

export const getPlants = async (): Promise<Plant[]> => {
  return plants as Plant[];
};

export const getPlantDetails = async (id: string) => {
  const plant = plants.find((plant: Plant) => plant.id === id);
  if (!plant) {
    throw new Error(`Plant with id ${id} not found`);
  }
  return plant;
};
