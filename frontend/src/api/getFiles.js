import fetch from "./handler";

export const getResumes = () => {
  return fetch({
    method: "GET",
    url: "/resume",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
  });
};

export const uploadResume = async (formData) => {
  const res = await fetch({
    method: "POST",
    url: "/resume",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    body: formData,
  });
  return res;
};
