import { reqApi } from "./base";
import { api } from ".";

export const getNewWellForm = async () => {
  return (await reqApi("/geo/add")).data;
};

export const addNewWell = async (data) => {
  return (await reqApi("/geo/add", data, "POST")).data;
};

export const editWell = async (number, data) => {
  return (await reqApi(`/geo/${number}/edit`, data, "POST")).data;
};

export const getWells = async () => {
  return (await reqApi("/geo/")).data;
};

export const getWellsWithParameters = async (date) => {
  return (await reqApi(`/geo/with_parameters`, {date: date})).data;
};

export const getParameterDates = async () => {
  return (await reqApi(`/geo/parameter/dates`)).data;
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

export const uploadFile = async (well_number, file) => {
  const formData = new FormData();
  formData.append("file", file);
  const config = {
    method: 'POST',
    url: `/geo/${well_number}/upload`,
    headers: { 'Content-Type': 'multipart/form-data' },
    data: formData,
    onUploadProgress: progressEvent => {
      console.log("Upload Progress:", Math.round((progressEvent.loaded * 100) / progressEvent.total));
    },
  };

  const response = await api.request(config);
  return response;
};

export const sendExcelData = async (well_number, data) => {
  return (await reqApi(`/geo/${well_number}/parameter/bulk-add`, data, "POST")).data;
};

export const sendConfirmedExcelData = async (well_number, data) => {
  return (await reqApi(`/geo/${well_number}/parameter/bulk-add/confirmed`, data, "POST")).data;
};

export const deleteParameter = async (well_number, date) => {
  return (await reqApi(`/geo/parameter/delete`, {well: well_number, date: date}, "POST")).data;
};
