import axios from "axios";
const BASE_URL = "/api";

// 响应拦截 (这里以后写axios响应拦截)
axios.interceptors.response.use(
  (res) => {
    // 根据获取响应的信息的code的值 进行相对应的处理
    if (res.status == 200) {
        
      return res;
    } else {
      return Promise.reject(res.status);
    }
  },
  (err) => {
    Promise.reject(err.response);
  }
);

const requestPost = (url, params) => {
  return new Promise((resolve, reject) => {
    url = BASE_URL + url;
    axios
      .post(url, params)
      .then((res) => {
        resolve(res.data);
      })
      .catch((err) => {
        reject(err);
      });
  });
};

export const getRestaurant = (data) => requestPost("/user/apiFindUid", data);
export const getResList = (data) => requestPost("/user/apiBusiness", data);
