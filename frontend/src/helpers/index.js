export const dateWithoutTimezone = (date) => {
  const tzoffset = date.getTimezoneOffset() * 60000; //offset in milliseconds
  const withoutTimezone = new Date(date.valueOf() - tzoffset)
    .toISOString()
    .slice(0, -1);
  return withoutTimezone;
};

export const dateToISOString = (date) => {
  const year = parseInt(date.slice(0, 4), 10); // 2021
  const month = parseInt(date.slice(5, 7), 10) - 1; // 12 - 1 = 11 (December)
  const day = parseInt(date.slice(8, 10), 10); // 01
  return new Date(year, month, day);
};
