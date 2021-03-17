export const removeQuotes = (string: string) => {
  const hasQuotes = /^"([^"]+)"$/.exec(string);
  if (!hasQuotes) {
    return string;
  }
  const [, actualValue] = hasQuotes;
  return actualValue;
};
