const fs = require("fs-extra");
const path = require("path");

const areaItemsFile = path.resolve(__dirname, "./area-items.json");

/**
 * 解析城市信息
 */
const getAreaItems = () => {
  const res = fs.readJSONSync(areaItemsFile) || {};
  const cityInfo = {};

  res.forEach((item) => {
    item.children.forEach((child) => {
      cityInfo[child.value] = child.children;
    });
  });

  fs.writeJsonSync(path.resolve(__dirname, "./area-city.json"), cityInfo, { spaces: 2 });
};

const addAllDistrict = () => {
  const res = fs.readJSONSync(areaItemsFile) || {};

  res.forEach((item) => {
    item.children.forEach((child) => {
      child.children.unshift({ value: child.value, label: "全城" })
    });
  });

  fs.writeJsonSync(path.resolve(__dirname, "./area-all-distr.json"), res, { spaces: 2 });
};

addAllDistrict()
