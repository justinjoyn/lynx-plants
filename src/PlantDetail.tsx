import { useParams } from "react-router";

export const PlantDetail = () => {
  const { species } = useParams();

  return (
    <view>
      <text>{species}</text>
    </view>
  );
};
