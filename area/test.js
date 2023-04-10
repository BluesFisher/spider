const fs = require("fs-extra");
const path = require("path");
const request = require("request");

const mtFile = path.resolve(__dirname, "./area-mt.json");
const dzFile = path.resolve(__dirname, "./area-dz.json");
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

/* ------------------------ mt ------------------------ */
const MT = {
  key: {
    深圳市: 30,
    广州市: 20,
    佛山市: 92,
    东莞市: 91,
    上海市: 10,
    北京市: 1,
  }["上海市"],
  /**
   * 获取美团球场详细信息
   * @param {*} id
   * @returns
   */
  getMtDetail(id) {
    return new Promise((resolve) => {
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
  },

  /**
   * 过滤美团重复的id
   */
  filterMtId() {
    const res = fs.readJSONSync(mtFile) || [];
    let idList = [];
    const result = res.filter((item) => {
      const isFilter = !idList.includes(item.orgId);
      idList = [...new Set([...idList, item.orgId])];

      return isFilter;
    });
    console.log("file content: ", result.length);
    fs.writeJsonSync(mtFile, result, { spaces: 2 });
  },

  async dealMtData(item) {
    const { areaCode, orgAddr } = await parseLocation(item);
    const { tags, desc } = await this.getMtDetail(item.id);
    let note = "";
    let avgscoreShow = `评分：${item.avgscore}`;

    if (item.lowestprice) {
      note += `¥${item.lowestprice}起`;
    }

    if (item.avgscore === 0) {
      avgscoreShow = `评分：-`;
    } else if (`${item.avgscore}`.length === 1) {
      avgscoreShow = `评分：${item.avgscore}.0`;
    }

    item.deals &&
      item.deals.forEach((v) => {
        note += `，${v.title}-¥${v.price}`;
      });

    return {
      orgId: item.id,
      mtId: item.id,
      areaCode,
      latitude: item.latitude,
      longitude: item.longitude,
      orgName: item.title,
      orgAddr,
      note,
      score: item.avgscore,
      tags: [{ value: avgscoreShow, type: 2 }, ...tags],
      desc,
      phone: "",
    };
  },

  getMtSearch(offset = 0, keyword = "篮球场") {
    return new Promise((resolve) => {
      request.get(
        `https://apimobile.meituan.com/group/v4/poi/pcsearch/${
          this.key
        }?uuid=858ebe70fba8447f8468.1680836575.1.0.0&userid=3933147557&limit=32&offset=${offset}&cateId=-1&q=${encodeURIComponent(
          keyword
        )}&token=AgGeIzjjm83bB8OmCKag5O8oGKJByTN_99OY49jwPG0WhUN3xUOZ7mg2qwMk0YpV_Qv9IhqXDGdcxwAAAAC2FwAAeKs0mikJ_CFrHiXfnebmV1yyONq6x51ya77XfHss7aGps2SJanTPWnUMreIzuc-y`,
        {
          headers: {
            Cookie:
              "_ga=GA1.1.1431178464.1676274558; _ga_LYVVHCWVNG=GS1.1.1676274557.1.1.1676274801.0.0.0; uuid=858ebe70fba8447f8468.1680836575.1.0.0; _lxsdk_cuid=18759aac3a0c8-0ef42e79fcca48-1e525634-1ea000-18759aac3a0c8; WEBDFPID=6u6y29ux278256w5zwu53308w3024vy381240zzx128979580w294u04-1996196577248-1680836576526GUASGOI75613c134b6a252faa6802015be905511013; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; iuuid=9F9F60BE215DAE299A4AB3A09C2032680D9F3FEA1DBA83B9BCDAE2C7A0753EC2; qruuid=9a7151a4-e008-4d2e-9828-35b954d2b2aa; token2=AgGeIzjjm83bB8OmCKag5O8oGKJByTN_99OY49jwPG0WhUN3xUOZ7mg2qwMk0YpV_Qv9IhqXDGdcxwAAAAC2FwAAeKs0mikJ_CFrHiXfnebmV1yyONq6x51ya77XfHss7aGps2SJanTPWnUMreIzuc-y; oops=AgGeIzjjm83bB8OmCKag5O8oGKJByTN_99OY49jwPG0WhUN3xUOZ7mg2qwMk0YpV_Qv9IhqXDGdcxwAAAAC2FwAAeKs0mikJ_CFrHiXfnebmV1yyONq6x51ya77XfHss7aGps2SJanTPWnUMreIzuc-y; lt=AgGeIzjjm83bB8OmCKag5O8oGKJByTN_99OY49jwPG0WhUN3xUOZ7mg2qwMk0YpV_Qv9IhqXDGdcxwAAAAC2FwAAeKs0mikJ_CFrHiXfnebmV1yyONq6x51ya77XfHss7aGps2SJanTPWnUMreIzuc-y; u=3933147557; n=bIs495463988; _lxsdk=9F9F60BE215DAE299A4AB3A09C2032680D9F3FEA1DBA83B9BCDAE2C7A0753EC2; unc=bIs495463988; ci=20; rvct=20%2C30; firstTime=1681103642511; _lxsdk_s=187697a9f53-6a9-4f1-881%7C%7C140",
            Host: "apimobile.meituan.com",
            Origin: "https://sz.meituan.com",
            Pragma: "no-cache",
            Referer: "https://sz.meituan.com/",
            "User-Agent":
              " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
          },
        },
        (err, res) => {
          if (!err && res.statusCode === 200) {
            const { data } = JSON.parse(res.body || "{}");
            console.log("getMtSearch ok: ", keyword, offset);
            resolve(data.searchResult);
          } else {
            console.log("getMtSearch err: ", err, res);

            resolve({});
          }
        }
      );
    });
  },

  /**
   * 获取美团信息
   */
  async getMtData() {
    let allId = [];
    let res = [];
    for (let index = 0; index < 40; index++) {
      const offset = index * 32;
      const data = await this.getMtSearch(offset);

      for (let i = 0; i < data?.length; i++) {
        const item = data[i];
        if (allId.includes(item.id)) {
          console.log("repeat: ", { id: item.id, i });
          continue;
        }
        const result = await this.dealMtData(item);

        res.push(result);
        allId.push(item.id);

        console.log("ok: ", { id: item.id, i });

        if (i > 0 && i % 10 === 0) {
          const text = fs.readJSONSync(mtFile);
          fs.writeJsonSync(mtFile, [...text, ...res], { spaces: 2 });
          res = [];
        }

        await sleep();
      }

      const text = fs.readJSONSync(mtFile);
      fs.writeJsonSync(mtFile, [...text, ...res], { spaces: 2 });
      res = [];

      await sleep();
    }
    this.filterMtId();
  },

  /**
   * 获取不在大众点评里的美团
   */
  async getDiffMtData() {
    const { notInMt = [] } = fs.readJSONSync(notFile) || {};

    for (let i = 0; i < notInMt.length; i++) {
      const item = notInMt[i];
      const data = await this.getMtSearch(0, item);
      if (!data?.[0]) {
        console.log("getDiffMtData mt fail: ", item);
      } else {
        const result = await this.dealMtData(data?.[0]);
        const text = fs.readJSONSync(mtFile);
        fs.writeJsonSync(mtFile, [...text, result], { spaces: 2 });
        console.log("getDiffMtData mt ok: ", item);
      }

      await sleep();
    }
  },

  setMtElement() {
    let res = fs.readJSONSync(mtFile) || {};
    res = res.map((item) => {
      if (item.score === 0) {
        item.tags[0].value = `评分：-`;
      } else if (`${item.score}`.length === 1) {
        item.tags[0].value = `评分：${item.score}.0`;
      }

      return {
        ...item,
        mtId: item.orgId,
      };
    });
    console.log("file content: ", res.length);
    fs.writeJsonSync(mtFile, res, { spaces: 2 });
  },
};
/* ------------------------ mt ------------------------ */

/* ------------------------ dz ------------------------ */

const DZ = {
  headers: {
    wechatversion: "8.0.34",
    channel: "weixin",
    openidPlt: "oPpUI0S36sRzCeTW65UvK9ACTIAM",
    sdkversion: "2.30.4",
    openid: "gOlaMhukk0FfO6NnG6to3duXaM6SOdsv1JWT8XLcBvc",
    platform: "Android",
    platformversion: "15.5",
    dpid: "gOlaMhukk0FfO6NnG6to3duXaM6SOdsv1JWT8XLcBvc",
    minaname: "dianping-wxapp",
    appName: "dianping-wxapp",
    minaversion: "9.30.1",
    channelversion: "8.0.34",
    appVersion: "9.30.1",
    sdkversion: "2.30.2",
    token:
      "7af4354783a4a126c4794808b4fd7cf7a053ab98aa93b9488a29bb3f8b9072fbdbc95f13875b611e9b37adf73325c7aee0ad95c7bbbe80b7f6cffaa498acf2d60b4753cada74f91a9bf36066c04796c7b0a233bbdaf9c37e4fa28e7c377347c2",
    Referer: "https://servicewechat.com/wx734c1ad7b3562129/391/page-frame.html",
    "User-Agent":
      "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.34(0x18002230) NetType/WIFI Language/zh_CN",
  },
  /**
   * 获取大众点评篮球场详细信息，h5的headers
   * @param {*} item
   * @returns
   */
  getDzDetail(item) {
    return new Promise((resolve) => {
      request.get(
        `https://mapi.dianping.com/mapi/wechat/shop.bin?shopUuid=${item.shopUuid}&shopuuid=${item.shopUuid}`,
        {
          headers: {
            Host: "mapi.dianping.com",
            ...this.headers,
            isMicroMessenger: true,
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
            console.log("getDzDetail err: ", item.shopUuid, err, res);

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
  },

  /**
   * 获取大众点评列表， 小程序的headers
   * @param {*} index
   * @returns
   */
  getDzList(index = 0, keyword = "篮球场") {
    return new Promise((resolve) => {
      request.get(
        `https://m.dianping.com/wxmapi/search?cityId=7&locateCityid=7&lat=22.60956144876099&lng=114.12653115188573&myLat=22.60956144876099&myLng=114.12653115188573&keyword=${encodeURIComponent(
          keyword
        )}&start=${index * 10}`,
        {
          headers: {
            Host: "m.dianping.com",
            ...this.headers,
          },
        },
        (err, res) => {
          if (!err && res.statusCode === 200) {
            const { data } = JSON.parse(res.body || "{}");
            console.log("getDzList ok: ", index, keyword);
            resolve(data.list);
          } else {
            console.log("getDzList err: ", index, err, res);

            resolve([]);
          }
        }
      );
    });
  },

  async dealDzData(item) {
    const { orgAddr, phone, latitude, longitude, desc } =
      await this.getDzDetail(item);
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
  },

  /**
   * 获取大众点评篮球场信息
   */
  async getDzData() {
    for (let index = 40; index < 60; index++) {
      const data = (await this.getDzList(index)) || [];
      let res = [];

      for (let i = 0; i < data.length; i++) {
        const item = data[i].shopInfo;
        const result = await this.dealDzData(item);

        res.push(result);

        console.log("ok: ", { id: item.shopUuid, i, index });

        await sleep();
      }

      const text = fs.readJSONSync(dzFile);
      fs.writeJsonSync(dzFile, [...text, ...res], { spaces: 2 });
    }
  },

  filterDz() {
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
  },

  /**
   * 获取不在美团里的大众点评
   */
  async getDiffDzData() {
    const { notInDz = [] } = fs.readJSONSync(notFile) || {};

    for (let i = 0; i < notInDz.length; i++) {
      const item = notInDz[i];
      const data = await this.getDzList(0, item);
      if (!data?.[0]?.shopInfo) {
        console.log("getDiffDzData fail err: ", item);
      } else {
        const result = await this.dealDzData(data?.[0]?.shopInfo);
        const text = fs.readJSONSync(dzFile);
        fs.writeJsonSync(dzFile, [...text, result], { spaces: 2 });
        console.log("getDiffDzData dz ok: ", item);
      }

      await sleep();
    }
  },
};

/* ------------------------ dz ------------------------ */

const compare = () => {
  let mt = fs.readJSONSync(mtFile) || {};
  let dz = fs.readJSONSync(dzFile) || {};
  let notInDz = [];
  let notInMt = [];
  let mtSameName = [];
  let combine = [];

  mt.forEach((item) => {
    if (mt.filter((v) => v.orgName === item.orgName)?.length > 1) {
      mtSameName.push({
        orgName: item.orgName,
        latitude: item.latitude,
        longitude: item.longitude,
      });
    }

    const latMatch = dz.find(
      (v) =>
        `${v.latitude}`.startsWith(`${item.latitude}`) &&
        `${v.longitude}`.startsWith(`${item.longitude}`)
    );
    const nameMatch = dz.find((v) => v.orgName === item.orgName);
    let resultMatch = latMatch || nameMatch;

    if (resultMatch) {
      resultMatch = JSON.parse(JSON.stringify(latMatch || nameMatch));
      const desc = item.desc || resultMatch.desc;
      const phone = item.phone || resultMatch.phone;
      delete resultMatch.orgId;
      delete resultMatch.latitude;
      delete resultMatch.longitude;
      delete resultMatch.orgName;
      delete resultMatch.orgAddr;
      delete resultMatch.areaCode;
      delete resultMatch.desc;
      delete resultMatch.phone;
      combine.push({ ...item, desc, phone, dzInfo: resultMatch });
    } else {
      combine.push(item);
      notInDz.push(item.orgName);
    }
  });

  dz.forEach((item) => {
    if (!mt.find((v) => v.orgName === item.orgName)) {
      notInMt.push(item.orgName);
    }
  });

  mtSameName = mtSameName.sort((a, b) => (a.orgName <= b.orgName ? 1 : -1));

  console.log(
    "notInDz: ",
    notInDz.length,
    "notInMt: ",
    notInMt.length,
    "mtSameName: ",
    mtSameName.length,
    "combine: ",
    combine.length
  );

  fs.writeJsonSync(notFile, { notInDz, notInMt, mtSameName }, { spaces: 2 });
  fs.writeJsonSync("./combine.json", combine, { spaces: 2 });
};

MT.getMtData();
// MT.setMtElement();
// MT.filterMtId();
// MT.getDiffMtData();
// MT.getMtSearch();

// DZ.getDzData();
// DZ.getDiffDzData();

// compare();
