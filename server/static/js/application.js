window.sm = 768;
window.md = 992;
window.lg = 1200;
window.xl = 1920;

/**
 * 判断一个对象或字符串是否为空
 */
window.isEmpty = obj => {
    return obj === null || obj === undefined || obj === '';
};

/**
 * 判断数组是否为空
 */
window.isArrEmpty = arr => {
    return !isEmpty(arr) && arr.length === 0;
};

/**
 * 浅复制数组内容
 */
window.copyArr = function (dest, src) {
    dest.splice(0);
    for (let i in src) {
        dest.push(src[i]);
    }
};

/**
 * 浅度克隆对象
 */
window.clone = function(obj) {
    let newObj = obj instanceof Array ? [] : {};
    for (let prop in obj) {
        newObj[prop] = obj[prop];
    }
    return newObj;
};

/**
 * 深度克隆对象
 */
window.deepClone = function(obj) {
    let newObj = obj instanceof Array ? [] : {};
    for (let prop in obj) {
        let value = obj[prop];
        newObj[prop] = typeof value === 'object' ? deepClone(value) : value;
    }
    return newObj;
};

/**
 * 将 src 对象中的所有属性浅复制到 dest 中
 */
window.cloneProp = function(dest, src, ignoreProps) {
    let ignoreEmpty = isEmpty(ignoreProps);
    for (let key in src) {
        if (ignoreEmpty) {
            dest[key] = src[key];
        } else {
            let ignore = false;
            for (let i = 0; i < ignoreProps.length; ++i) {
                if (key === ignoreProps[i]) {
                    ignore = true;
                    break;
                }
            }
            if (!ignore) {
                dest[key] = src[key];
            }
        }
    }
};

/**
 * 执行函数
 */
window.execute = (func, ... args) => {
    if (func !== undefined && typeof func === 'function') {
        switch(args.length) {
            case 0: func(); break;
            case 1: func(args[0]); break;
            case 2: func(args[0], args[1]); break;
            case 3: func(args[0], args[1], args[2]); break;
            case 4: func(args[0], args[1], args[2], args[3]); break;
            default: func(args); break;
        }
    }
};

/**
 * 获取 url 参数
 */
window.getUrlParams = () => {
    let search = location.search;
    let params = {};
    if (search.indexOf("?") !== -1) {
        let str = search.substring(1);
        let keyValues = str.split("&");
        for(let i = 0; i < keyValues.length; i ++) {
            let keyValue = keyValues[i].split("=");
            params[decodeURIComponent(keyValue[0])] = decodeURIComponent(keyValue[1]);
        }
    }
    return params;
};

/**
 * 获取 url [name] 参数的值
 */
window.getUrlParamValue = name => {
    return getUrlParams()[name];
};

/**
 * 获取 url 中 # 后面的内容
 */
window.getUrlArg = () => {
    let hash = location.hash;
    if (isEmpty(hash)) {
        return '';
    } else {
        return hash.substring(1);
    }
};

/**
 * 初始化滚动条
 */
window.initScrollbars = () => {
    let scrollbars = [];
    let els = document.getElementsByClassName('gemini-scrollbar');
    for (let i = 0; i < els.length; ++i) {
        scrollbars.push(new Vue.$geminiScrollbar({
            element: els[i]
        }).create());
    }
    return scrollbars;
};

/**
 * 获取 body 宽度
 */
window.bodyWidth = () => {
    return document.body.clientWidth;
};

/**
 * 初始化侧边栏
 */
window.initVuejs = vm => {
    window.onresize = function () {
        vm.isCollapse = needCollapse();
    };
};

let ONE_KB = 1024;
let ONE_MB = ONE_KB * 1024;
let ONE_GB = ONE_MB * 1024;
let ONE_TB = ONE_GB * 1024;
let ONE_PB = ONE_TB * 1024;

window.sizeFormat = size => {
    if (size < ONE_KB) {
        return size.toFixed(0) + " B";
    } else if (size < ONE_MB) {
        return (size / ONE_KB).toFixed(2) + " KB";
    } else if (size < ONE_GB) {
        return (size / ONE_MB).toFixed(2) + " MB";
    } else if (size < ONE_TB) {
        return (size / ONE_GB).toFixed(2) + " GB";
    } else if (size < ONE_PB) {
        return (size / ONE_TB).toFixed(2) + " TB";
    } else {
        return (size / ONE_PB).toFixed(2) + " PB";
    }
};

let seq = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
];

/**
 * 随机生成 min 至 max-1 之间的整数
 */
window.randomIntRange = (min, max) => {
    return parseInt(Math.random() * (max - min) + min, 10);
};

/**
 * 随机生成 0 至 n-1 之间的整数
 */
window.randomInt = n => {
    return randomIntRange(0, n);
};

/**
 * 随机生成 count 个字母和数字
 */
window.randomSeq = count => {
    let str = '';
    for (let i = 0; i < count; ++i) {
        str += seq[randomInt(62)];
    }
    return str;
};

window.randomLowerAndNum = count => {
    let str = '';
    for (let i = 0; i < count; ++i) {
        str += seq[randomInt(36)];
    }
    return str;
};

window.randomMTSecret = () => {
    let str = '';
    for (let i = 0; i < 32; ++i) {
        let index = randomInt(16);
        if (index <= 9) {
            str += index;
        } else {
            str += seq[index - 10];
        }
    }
    return str;
};

window.propIgnoreCase = (obj, prop) => {
    for (let name in obj) {
        if (name.toLowerCase() === prop.toLowerCase()) {
            return obj[name];
        }
    }
    return undefined;
};