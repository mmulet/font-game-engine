export const allColors = [
  "#007aff",
  "#34c759",
  "#33c6a2",
  "#007bff",
  "#5856d6",
  "#9855d6",
  "#00faff",
  "#5593d6",
  "#5ac8fa",
];

export const colors = [...new Array(2000).keys()].map(
  () => allColors[Math.floor(Math.random() * allColors.length)]
);
