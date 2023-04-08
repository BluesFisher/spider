const fs = require("fs-extra");
const path = require("path");
const request = require("request");

const mtFile = path.resolve(__dirname, "./area-mt.json");
const dzFile = path.resolve(__dirname, "./area-res.json");
const srcFile = path.resolve(__dirname, "./area.json");

const sleep = () =>
  new Promise((resolve) => {
    setTimeout(() => resolve({}), 5000);
  });

/**
 * 经纬度解析
 * @param {*} item { latitude, longitude }
 * @returns  { areaCode, orgAddr }
 */
const parseLocation = (item) =>
  new Promise((resolve) => {
    request(
      `https://apis.map.qq.com/ws/geocoder/v1/?location=${item.latitude},${item.longitude}&key=H4PBZ-EFZKX-WD44S-ZPRVX-QY457-MIFCV&get_poi=1`,
      (err, res) => {
        if (!err && res.statusCode === 200) {
          const area = JSON.parse(res.body || "{}");
          const { ad_info: adInfo, address } = area?.result || {};
          const { adcode: areaCode } = adInfo || {};

          resolve({ areaCode, orgAddr: address });
        } else {
          console.log("parseLocation err: ", item.id, err);

          resolve({ areaCode: "", orgAddr: "" });
        }
      }
    );
  });

/**
 * 获取美团球场详细信息
 * @param {*} id
 * @returns
 */
const getMtDetail = (id) =>
  new Promise((resolve) => {
    request(
      `https://i.meituan.com/nibmp/mva/gateway-proxy/poiext/shopbaseinfo?clientType=2&shopId=${id}&source=1&cityId=30`,
      (err, res) => {
        if (!err && res.statusCode === 200) {
          const { data } = JSON.parse(res.body || "{}");
          const tags =
            data?.shopTags?.map((item) => ({ value: item, type: 1 })) || [];

          resolve({ tags, desc: `营业时间：${data.businessHours}` });
        } else {
          console.log("getMtDetail err: ", id, err);

          resolve({ tags: [], desc: "" });
        }
      }
    );
  });

/**
 * 过滤美团重复的id
 */
const filterMtId = () => {
  const res = fs.readJSONSync(srcFile) || {};
  let idList = [];
  res.data.searchResult = res.data.searchResult.filter((item) => {
    const isFilter = !idList.includes(item.id);
    idList = [...new Set([...idList, item.id])];

    return isFilter;
  });
  console.log("file content: ", res.data.searchResult.length);
  fs.writeJsonSync(srcFile, res, { spaces: 2 });
};

/**
 * 获取美团信息
 */
const getMtData = async () => {
  filterMtId();
  const { data } = fs.readJSONSync(srcFile) || {};
  let res = [];

  for (let i = 0; i < data.searchResult?.length; i++) {
    const item = data.searchResult[i];
    const { areaCode, orgAddr } = await parseLocation(item);
    const { tags, desc } = await getMtDetail(item.id);
    let note = "";

    if (item.lowestprice) {
      note += `¥${item.lowestprice}起`;
    }

    item.deals &&
      item.deals.forEach((v) => {
        note += `，${v.title}-¥${v.price}`;
      });

    res.push({
      orgId: item.id,
      areaCode,
      latitude: item.latitude,
      longitude: item.longitude,
      orgName: item.title,
      orgAddr,
      note,
      score: item.avgscore,
      tags: [{ value: `评分：${item.avgscore || "-"}`, type: 2 }, ...tags],
      desc,
      phone: "",
    });

    console.log("ok: ", { id: item.id, i });

    if (i > 0 && i % 10 === 0) {
      const text = fs.readJSONSync(mtFile);
      fs.writeJsonSync(mtFile, [...text, ...res], { spaces: 2 });
      res = [];
    }

    await sleep();
  }

  const text = fs.readJSONSync(mtFile);
  fs.writeJSON(mtFile, [...text, ...res], { spaces: 2 });
};

const setMtElement = () => {
  let res = fs.readJSONSync(mtFile) || {};
  res = res.map((item) => {
    const v = item.tags[0].value.replace("评分：", "");

    return {
      ...item,
      mtId: item.orgId,
    };
  });
  console.log("file content: ", res.length);
  fs.writeJsonSync(mtFile, res, { spaces: 2 });
};

// getMtData();
// setMtElement()

const getDzData = async () => {
  // filterMtId();
  const { data } = fs.readJSONSync(srcFile) || {};
  let res = [];

  for (let i = 0; i < data.length; i++) {
    const item = data[i].shopInfo;
    item.latitude = item.myLat;
    item.longitude = item.myLng;
    const { areaCode, orgAddr } = await parseLocation(item);
    let note = item.recommendReason?.text || "";

    const tags = (item.tagList || []).map((v) => ({
      value: v.text,
      type: v.textColor === "#B15E2C" ? 2 : 1,
    }));

    res.push({
      orgId: item.shopUuid,
      dzId: item.shopUuid,
      dzPath: item.navData?.url,
      areaCode,
      latitude: item.latitude,
      longitude: item.longitude,
      orgName: item.name + item.branchName ? `(${item.branchName})` : "",
      orgAddr,
      note,
      score: +item.starScore,
      tags: [{ value: `评分：${item.starScore || "-"}`, type: 2 }, ...tags],
      desc,
      phone: "",
    });

    console.log("ok: ", { id: item.id, i });

    if (i > 0 && i % 10 === 0) {
      const text = fs.readJSONSync(dzFile);
      fs.writeJsonSync(dzFile, [...text, ...res], { spaces: 2 });
      res = [];
    }

    await sleep();
  }

  const text = fs.readJSONSync(dzFile);
  fs.writeJSON(dzFile, [...text, ...res], { spaces: 2 });
};

getDzData();
