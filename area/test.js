const fs = require("fs-extra");
const path = require("path");
const request = require("request");

const mtFile = path.resolve(__dirname, "./area-mt.json");
const dzFile = path.resolve(__dirname, "./area-dz.json");
const resFile = path.resolve(__dirname, "./area-res.json");
const srcFile = path.resolve(__dirname, "./area.json");
const notFile = path.resolve(__dirname, "./not.json");

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

/**
 * 获取大众点评篮球场详细信息，h5的headers
 * @param {*} item
 * @returns
 */
const getDzDetail = (item) =>
  new Promise((resolve) => {
    request.get(
      `https://mapi.dianping.com/mapi/wechat/shop.bin?shopUuid=${item.shopUuid}&shopuuid=${item.shopUuid}`,
      {
        headers: {
          Cookie:
            "seouser_ab=ugcdetail%3AA%3A1; _lxsdk_cuid=18759a1439bc8-08b58ca907344d-1e525634-1ea000-18759a1439bc8; _lxsdk=18759a1439bc8-08b58ca907344d-1e525634-1ea000-18759a1439bc8; _hc.v=962e2f7f-8566-5bdc-3a6f-07457415888d.1680835955; WEBDFPID=zvw58853xw5u518vz5w5y704w1v0495w81240z85z7x979589wwy522z-1996195955101-1680835953717GGSAQEA75613c134b6a252faa6802015be905513328; fspop=test; cy=7; cye=shenzhen; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1680918479; s_ViewType=10; dper=563a4af6dd681d5a2dda291cad1aaff022d8d712f3de7a42344246637734a31c670e1bec687aa17aa5d22d7820834244aa9d3a9186c4ee0b73aaa03578a544e2; qruuid=402aca2a-bae9-4379-b121-e7e662400798; ll=7fd06e815b796be3df069dec7836c3df; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1680960824",
          Host: "mapi.dianping.com",
        },
      },
      (err, res) => {
        if (!err && res.statusCode === 200) {
          const { address, phoneNos, geoPoint, recentBizTime } = JSON.parse(
            res.body || "{}"
          );

          resolve({
            orgAddr: address,
            phone: phoneNos?.[0] || "",
            latitude: geoPoint?.lat,
            longitude: geoPoint?.lng,
            desc: `营业时间：${
              recentBizTime?.title?.replace(/\n/g, " ") || "-"
            }`,
          });
        } else {
          console.log("getDzDetail err: ", item.shopUuid, err);

          resolve({
            orgAddr: "",
            phone: "",
            latitude: "",
            longitude: "",
            desc: "",
          });
        }
      }
    );
  });

/**
 * 获取大众点评列表， 小程序的headers
 * @param {*} index
 * @returns
 */
const getDzList = (index = 0, keyword = "篮球场") =>
  new Promise((resolve) => {
    request.get(
      `https://m.dianping.com/wxmapi/search?cityId=7&locateCityid=7&lat=22.60956144876099&lng=114.12653115188573&myLat=22.60956144876099&myLng=114.12653115188573&keyword=${encodeURIComponent(
        keyword
      )}&start=${index * 10}`,
      {
        headers: {
          Host: "m.dianping.com",
          wechatversion: "8.0.34",
          "content-type": "application/json",
          channel: "weixin",
          openidPlt: "oPpUI0darwIbMvZxLeG8CgYWzZHY",
          sdkversion: "2.30.4",
          openid: "mWq3fmLuGZDgPhqFgvu_25T8UYXJVaa2VngiSW5_vwY",
          token:
            "279aa4474837b29d0d502fb9c43a28652b420bfef2e060dcdf44fed44cbcdfc2b5b744f30169ec7d122c6570b5777b80d539749021b9a3376bf633109e3ee4983cebba92c0c64782a5750269448fee2ca794b5c32b98977c8bb1b8868edfdaa2",
          platform: "Android",
          platformversion: "15.5",
          dpid: "mWq3fmLuGZDgPhqFgvu_25T8UYXJVaa2VngiSW5_vwY",
          minaname: "dianping-wxapp",
          minaversion: "9.30.1",
          channelversion: "8.0.34",
          Referer:
            "https://servicewechat.com/wx734c1ad7b3562129/391/page-frame.html",
          "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.34(0x18002230) NetType/WIFI Language/zh_CN",
        },
      },
      (err, res) => {
        if (!err && res.statusCode === 200) {
          const { data } = JSON.parse(res.body || "{}");
          console.log("getDzList ok: ", index);
          resolve(data.list);
        } else {
          console.log("getDzList err: ", index, err);

          resolve([]);
        }
      }
    );
  });

const dealDzData = async (item) => {
  const { orgAddr, phone, latitude, longitude, desc } = await getDzDetail(item);
  const { areaCode } = await parseLocation({ latitude, longitude });
  let note = item.recommendReason?.text || "";

  const tags = (item.tagList || []).map((v) => ({
    value: v.text,
    type: v.textColor === "#B15E2C" ? 2 : 1,
  }));

  return {
    orgId: item.shopUuid,
    dzId: item.shopUuid,
    dzPath: item.navData?.url,
    areaCode,
    latitude: latitude,
    longitude: longitude,
    orgName: item.name + (item.branchName ? `（${item.branchName}）` : ""),
    orgAddr,
    note,
    score: +item.starScore,
    tags: [
      {
        value: `评分：${`${item.starScore}`.slice(0, -1) || "-"}`,
        type: 2,
      },
      ...tags,
    ],
    desc,
    phone,
  };
};

/**
 * 获取大众点评篮球场信息
 */
const getDzData = async () => {
  for (let index = 40; index < 60; index++) {
    const data = (await getDzList(index)) || [];
    let res = [];

    for (let i = 0; i < data.length; i++) {
      const item = data[i].shopInfo;
      const result = await dealDzData(item);

      res.push(result);

      console.log("ok: ", { id: item.shopUuid, i, index });

      await sleep();
    }

    const text = fs.readJSONSync(dzFile);
    fs.writeJsonSync(dzFile, [...text, ...res], { spaces: 2 });
  }
};

const filterDz = () => {
  let dz = fs.readJSONSync(dzFile) || {};
  let dzRes = [];

  dz.forEach((item) => {
    if (!["贰木眼镜"].some((v) => item.orgName.includes(v))) {
      dzRes.push(item);
    }
  });

  let idList = [];
  dzRes = dzRes.filter((item) => {
    const isFilter = !idList.includes(item.orgId);
    idList = [...new Set([...idList, item.orgId])];

    return isFilter;
  });

  dz = dzRes;
  fs.writeJsonSync(dzFile, dzRes, { spaces: 2 });
};

const compare = () => {
  let mt = fs.readJSONSync(mtFile) || {};
  let dz = fs.readJSONSync(dzFile) || {};
  let notInDz = [];
  let notInMt = [];

  mt.forEach((item) => {
    if (!dz.find((v) => v.orgName === item.orgName)) {
      notInDz.push(item.orgName);
    }
  });

  dz.forEach((item) => {
    if (!mt.find((v) => v.orgName === item.orgName)) {
      notInMt.push(item.orgName);
    }
  });

  fs.writeJsonSync(notFile, { notInDz, notInMt }, { spaces: 2 });
};

const getDiffData = async () => {
  const { notInDz = [] } = fs.readJSONSync(notFile) || {};

  for (let i = 0; i < notInDz.length; i++) {
    const item = notInDz[i];
    const data = await getDzList(0, "上域·糖果篮球公园");
    if (!data?.[0]?.shopInfo) {
      console.log("getDiffData dz err: ", orgName);
    } else {
      const result = await dealDzData(data?.[0]?.shopInfo);
      const text = fs.readJSONSync(dzFile);
      fs.writeJsonSync(dzFile, [...text, result], { spaces: 2 });

      await sleep();
    }
  }
};

// getMtData();
// setMtElement()
// getDzData();
// compare();
getDiffData();
