const fs = require('fs-extra');
const path = require('path');
const request = require('request');

const aimFile = path.resolve(__dirname, './area-res.json');
const srcFile = path.resolve(__dirname, './area.json');
const areaItemsFile = path.resolve(__dirname, './area-items.json');

const parseLocation = (item) => new Promise((resolve) => {
  request(
    `https://apis.map.qq.com/ws/geocoder/v1/?location=${item.latitude},${item.longitude}&key=H4PBZ-EFZKX-WD44S-ZPRVX-QY457-MIFCV&get_poi=1`,
    (err, res) => {
      if (!err && res.statusCode === 200) {
        const area = JSON.parse(res.body || '{}');
        const { ad_info: adInfo, address } = area?.result || {};
        const { adcode: areaCode } = adInfo || {};

        resolve({ areaCode, orgAddr: address });
      } else {
        console.log('parseLocation err: ', item.id, err);

        resolve({ areaCode: '', orgAddr: '' });
      }
    },
  );
});

const getDetail = (id) =>
  new Promise((resolve) => {
    request(
      `https://i.meituan.com/nibmp/mva/gateway-proxy/poiext/shopbaseinfo?clientType=2&shopId=${id}&source=1&cityId=30`,
      (err, res) => {
        if (!err && res.statusCode === 200) {
          const { data } = JSON.parse(res.body || '{}');
          const tags = data?.shopTags?.map(item => ({ value: item, type: 1 })) || [];

          resolve({ tags, desc: `营业时间：${data.businessHours}` });
        } else {
          console.log('getDetail err: ', id, err);

          resolve({ tags: [], desc: '' });
        }
      },
    );
  });

const sleep = () => new Promise((resolve) => {
  setTimeout(() => resolve({}), 5000);
});

const getData = async () => {
  const { data } = fs.readJSONSync(srcFile) || {};
  let res = [];

  for (let i = 0; i < data.searchResult?.length; i++) {
    const item = data.searchResult[i];
    const { areaCode, orgAddr } = await parseLocation(item);
    const { tags, desc } = await getDetail(item.id);
    let note = '';

    if (item.lowestprice) {
      note += `¥${item.lowestprice}起`;
    }

    item.deals && item.deals.forEach(v => {
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
      tags: [{ value: `评分：${item.avgscore || '-'}`, type: 2 }, ...tags],
      desc,
      phone: '',
    });

    console.log('ok: ', { id: item.id, i });

    if (i > 0 && i % 10 === 0) {
      const text = fs.readJSONSync(aimFile);
      fs.writeJsonSync(aimFile, [...text, ...res], { spaces: 2 });
      res = [];
    }

    await sleep();
  }

  const text = fs.readJSONSync(aimFile);
  fs.writeJSON(aimFile, [...text, ...res], { spaces: 2 });
};

const filterId = () => {
  const res = fs.readJSONSync(srcFile) || {};
  let idList = [];
  res.data.searchResult = res.data.searchResult.filter(item => {
    const isFilter = !idList.includes(item.id);
    idList = [...new Set([...idList, item.id])];

    return isFilter;
  });
  console.log('file content: ', res.data.searchResult.length);
  fs.writeJsonSync(srcFile, res, { spaces: 2 });
};

const getAreaItems = () => {
  const res = fs.readJSONSync(areaItemsFile) || {};
  const cityInfo = {};

  res.forEach(item => {
    item.children.forEach(child => {
      cityInfo[child.value] = child.children;
    });
  });

  fs.writeJsonSync('./area-city.json', cityInfo, { spaces: 2 });
};

const setElement = () => {
  let res = fs.readJSONSync(aimFile) || {};
  res = res.map(item =>{
    const v = item.tags[0].value.replace('评分：', '')

    return {
      ...item,
      score: v === '-' ? 0 : +v
  }
  })
  console.log('file content: ', res.length);
  fs.writeJsonSync(aimFile, res, { spaces: 2 });
};

// console.log(data);
// filterId();
// getData();
// getAreaItems();
setElement()
