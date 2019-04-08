// 脚本用于获取滑块验证码的人工轨迹，分为两部分，直接在 console 中运行即可

// 第一步：监听滑块拖动并生成距离列表，执行后需手动进行滑动验证，验证成功后再执行第二步
let arr=[0];
let startTime = Date.now();
let time = 10;
let timer;
let sp = $('#nc_1_n1z');  // 滑块元素
sp.onmousemove = function throttle(){  // 节流方式获取距离列表
    let left = parseInt(sp.style.left)
    let currentTime = Date.now();
    if(currentTime - startTime >= time){
        if(left>0&&left<258){
                arr.push(left)
        }
        startTime = currentTime;
    }else{
        clearTimeout(timer);
        timer = setTimeout(function () {
            throttle()
        }, 10);
    }
}

// 第二步：将距离列表处理成人工轨迹列表
let a = arr[1]
arr.splice(1,0,parseInt(a/2))
arr.push(258)
console.log(arr)

function fn(arr){
    let newArr = []
    let sum=0;
    arr.reduce((pro,item)=>{
        newArr.push(item-pro)
        return item
    },0)
    newArr.splice(0,1)
    sum  = newArr.reduce((a,b)=>{
        return a+b
    },0)
    console.log(sum)
    return newArr
}
fn(arr)