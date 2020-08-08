let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: getCookie('username'),
        f1_tab: 1, // 1F 标签页控制
        f2_tab: 1, // 2F 标签页控制
        f3_tab: 1, // 3F 标签页控制

        // 渲染首页购物车数据
        cart_total_count: 0,
        carts: [],
    },
    mounted() {
        // 获取cookie中的用户名
        this.username = getCookie('username');
    },
    methods: {
        // 获取简单购物车数据
        get_carts() {
            let url = '/carts/simple/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.carts = response.data.cart_skus;
                    this.cart_total_count = 0;
                    for (let i = 0; i < this.carts.length; i++) {
                        if (this.carts[i].name.length > 25) {
                            this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                        }
                        this.cart_total_count += this.carts[i].count;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        verify_user() {
            let sign = getCookie('sign');
            let url = `/has_expired/?sign=${sign}`
            axios.get(url, {
                responseType: 'json'
            }).then(response => {
                let backend_ret = response.data

                if (backend_ret.code == 0) {
                    console.log(backend_ret.errmsg)
                } else if (backend_ret.code == 4004) {
                    if (getCookie('username')) {
                        alert('该账号已在别处登录,请重新登录')
                        document.cookie = 'username=' + ''
                    }

                } else {
                    console.log(backend_ret)
                }
            }).catch(error => {
                console.log(error.response);
            })
        }
    }
});