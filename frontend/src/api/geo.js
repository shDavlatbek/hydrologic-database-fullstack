import { reqApi } from "./base";

export const getNewWellForm = async () => {
  return (await reqApi("/geo/add")).data;
};

export const addNewWell = async (data) => {
  return (await reqApi("/geo/add", data, "POST")).data;
};

export const getWells = async () => {
  return (await reqApi("/geo/")).data;
};

export const getWell = async (id) => {
  return (await reqApi(`/geo/${id}`)).data;
};

export const getParameterNames = async () => {
  return (await reqApi(`/parameter-names`)).data;
};

export const getParameter = async (well_number) => {
  return (await reqApi(`/geo/parameter`, {well: well_number})).data;
};

export const getPredictions = async (well_number) => {
  return (await reqApi(`/geo/parameter/predict`, {well_number: well_number})).data;
};