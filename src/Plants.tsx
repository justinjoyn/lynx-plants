import { useNavigate } from "react-router";
import { PlantList } from "./PlantList.jsx";
import "./Plants.css";

export const Plants = () => {
  const nav = useNavigate();

  return (
    <view class="content">
      <PlantList />
    </view>
  );
};
