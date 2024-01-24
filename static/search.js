
    var table = document.querySelector("table")
    var json = document.getElementById("dataid").getAttribute('d')
    var ul = document.querySelector(".u-list-control");
    var page_number = 5; //单页浏览的条数
    var Total_pages; //页数
    var liAll; //页码按钮下标为 1到length-2是页数 0和length-1为上一页和下一页
    var pre; //上一页
    var next; //下一页

    function clearTable() {
        table.innerHTML = `
        <div class="u-repeater u-repeater-1"><!--blog_post-->
        </div>
        `
    }
    window.onload = function() {
        json.forEach(function(item, i) {
            var tbody = document.querySelector(".u-repeater u-repeater-1");
            if (i < page_number) {
                var tr = document.createElement("div");
                tr.setAttribute('class','u-blog-post u-container-style u-repeater-item u-shape-rectangle')
                tr.innerHTML = `
                <div class="u-container-layout u-similar-container u-container-layout-1">
                  <div class="u-clearfix u-group-elements u-group-elements-3">
                    <a class="u-post-header-link" href=${item.url } style="float: left;"><!--blog_post_image-->
                      <img alt="" class="u-blog-control u-image u-image-default u-image-1" src="/static/images/0fd3416c.jpeg"><!--/blog_post_image-->
                    </a><!--blog_post_header--> 
                    <h2 class="u-align-left u-text u-text-default" >
                      <a class="u-post-header-link" href=${ item.url }"><!--blog_post_header_content-->${ item.head }<!--/blog_post_header_content--></a>
                    </h2><!--/blog_post_header--><!--blog_post_content-->
                    <p></p>
                    <div class="u-align-left u-blog-control u-post-content u-text u-text-default" style="left: 285px;"><!--blog_post_content_content-->{{ d.text|safe }}<!--/blog_post_content_content--></div><!--/blog_post_content--><!--blog_post_metadata-->
                    <div class="u-blog-control u-metadata u-text-grey-40 u-metadata-1"><!--blog_post_metadata_date-->
                      <span class="u-meta-date u-meta-icon"><!--blog_post_metadata_date_content-->Sat Nov 19 2022<!--/blog_post_metadata_date_content--></span><!--/blog_post_metadata_date--><!--blog_post_metadata_comments-->
                      <span class="u-meta-comments u-meta-icon"><!--blog_post_metadata_comments_content-->Comments (0)<!--/blog_post_metadata_comments_content--></span><!--/blog_post_metadata_comments-->
                    </div><!--/blog_post_metadata-->
                  </div>
                </div>
                           `
                tbody.appendChild(tr);
            }

        })

        var len = json.length; //总记录条数

        Total_pages = len % page_number == 0 ? len / page_number : len / page_number + 1; //页数

        for (var i = 1; i <= Total_pages; i++) {
            ul.innerHTML += `
            <li class="active u-nav-item u-pagination-item" id="${i}">
                <a class="u-button-style u-nav-link" href="#" style="padding: 16px 28px;">${i}</a>
              </li>
            `
        }

        ul.innerHTML += `
        <li class="next u-nav-item u-pagination-item">
        <a class="u-button-style u-nav-link" href="#" style="padding: 16px 28px;">〉</a>
      </li>
        `;
        liAll = document.querySelectorAll("li");
        liAll[1].childNodes[0].style.color = "red"; //初始第一页页码是红的
        // console.log([liAll])
        var pagethis = 1; //当前是第几页
        for (var i = 1; i < liAll.length - 1; i++) {
            liAll[i].onclick = function() {
                for (var j = 1; j < liAll.length - 1; j++) {
                    liAll[j].childNodes[0].style.color = "blue"
                }
                pagethis = this.id; //获取当前是第几页
                liAll[pagethis].childNodes[0].style.color = "red";
                // console.log(liAll[i])
                let start; //当页数据的起始下标
                let end; //当页数据的结束下标
                if (pagethis != 1) {
                    start = (pagethis - 1) * page_number;
                    end = start + page_number;
                    if (end > json.length - 1) { //如果当页数据结束值大于总数据条数下标的值则赋值为总数据条数最大下标值
                        end = json.length - 1;
                    }
                } else {
                    start = 0;
                    end = page_number - 1;
                }
                // console.log("start=" + start)
                // console.log("end=" + end)
                clearTable();
                var tbody = document.querySelector(".u-repeater u-repeater-1");
                json.forEach(function(item, i) {

                    if (i >= start && i <= end) {
                        var tr = document.createElement("div");
                        tr.setAttribute('class','u-blog-post u-container-style u-repeater-item u-shape-rectangle')
                        tr.innerHTML = `
                <div class="u-container-layout u-similar-container u-container-layout-1">
                  <div class="u-clearfix u-group-elements u-group-elements-3">
                    <a class="u-post-header-link" href=${item.url } style="float: left;"><!--blog_post_image-->
                      <img alt="" class="u-blog-control u-image u-image-default u-image-1" src="/static/images/0fd3416c.jpeg"><!--/blog_post_image-->
                    </a><!--blog_post_header--> 
                    <h2 class="u-align-left u-text u-text-default" >
                      <a class="u-post-header-link" href=${ item.url }"><!--blog_post_header_content-->${ item.head }<!--/blog_post_header_content--></a>
                    </h2><!--/blog_post_header--><!--blog_post_content-->
                    <p></p>
                    <div class="u-align-left u-blog-control u-post-content u-text u-text-default" style="left: 285px;"><!--blog_post_content_content-->{{ d.text|safe }}<!--/blog_post_content_content--></div><!--/blog_post_content--><!--blog_post_metadata-->
                    <div class="u-blog-control u-metadata u-text-grey-40 u-metadata-1"><!--blog_post_metadata_date-->
                      <span class="u-meta-date u-meta-icon"><!--blog_post_metadata_date_content-->Sat Nov 19 2022<!--/blog_post_metadata_date_content--></span><!--/blog_post_metadata_date--><!--blog_post_metadata_comments-->
                      <span class="u-meta-comments u-meta-icon"><!--blog_post_metadata_comments_content-->Comments (0)<!--/blog_post_metadata_comments_content--></span><!--/blog_post_metadata_comments-->
                    </div><!--/blog_post_metadata-->
                  </div>
                </div>
                           `
                tbody.appendChild(tr);
                    }
                })

            }
        }
        // pre = document.querySelector("#pre") //上一页
        // next = document.querySelector("#next") //下一页
        // pre.onclick = function() {
        //     // alert(pagethis)
        //     if (pagethis != 1) { //当前页数不等于1时执行上一页
        //         pagethis--;
        //         for (var j = 1; j < liAll.length - 1; j++) {
        //             liAll[j].childNodes[0].style.color = "blue"
        //         }
        //         liAll[pagethis].childNodes[0].style.color = "red";
        //         let start;
        //         let end;
        //         if (pagethis != 1) {
        //             start = (pagethis - 1) * page_number;
        //             end = start + page_number;
        //             if (end > json.length - 1) {
        //                 end = json.length - 1;
        //             }
        //         } else {
        //             start = 0;
        //             end = page_number - 1;
        //         }

        //         clearTable();
        //         var tbody = document.querySelector("tbody");
        //         json.forEach(function(item, i) {
        //             if (i >= start && i <= end) {
        //                 var tr = document.createElement("tr");
        //                 tr.innerHTML = `
        //                     <td>${item.product_name}</td>
        //                     <td>${item.price}</td>
        //                     <td>${item.imgurl}</td>
        //                     `
        //                 console.log(tr)
        //                 tbody.appendChild(tr);
        //             }
        //         })
        //     }
        // }
        // next.onclick = function() {
        //     // alert(pagethis)
        //     if (pagethis < liAll.length - 2) { //当前页数小于最后一页则执行下一页
        //         pagethis++;
        //         for (var j = 1; j < liAll.length - 1; j++) {
        //             liAll[j].childNodes[0].style.color = "blue"
        //         }
        //         liAll[pagethis].childNodes[0].style.color = "red";
        //         let start;
        //         let end;
        //         if (pagethis != 1) {
        //             start = (pagethis - 1) * page_number;
        //             end = start + page_number;
        //             if (end > json.length - 1) {
        //                 end = json.length - 1;
        //             }
        //         } else {
        //             start = 0;
        //             end = page_number - 1;
        //         }

        //         clearTable();
        //         var tbody = document.querySelector("tbody");
        //         json.forEach(function(item, i) {
        //             if (i >= start && i <= end) {
        //                 var tr = document.createElement("tr");
        //                 tr.innerHTML = `
        //                 <div class="u-container-layout u-similar-container u-container-layout-1">
        //                 <div class="u-clearfix u-group-elements u-group-elements-3">
        //                   <a class="u-post-header-link" href=${item.url } style="float: left;"><!--blog_post_image-->
        //                     <img alt="" class="u-blog-control u-image u-image-default u-image-1" src="/static/images/0fd3416c.jpeg"><!--/blog_post_image-->
        //                   </a><!--blog_post_header--> 
        //                   <h2 class="u-align-left u-text u-text-default" >
        //                     <a class="u-post-header-link" href=${ item.url }"><!--blog_post_header_content-->${ item.head }<!--/blog_post_header_content--></a>
        //                   </h2><!--/blog_post_header--><!--blog_post_content-->
        //                   <p></p>
        //                   <div class="u-align-left u-blog-control u-post-content u-text u-text-default" style="left: 285px;"><!--blog_post_content_content-->{{ d.text|safe }}<!--/blog_post_content_content--></div><!--/blog_post_content--><!--blog_post_metadata-->
        //                   <div class="u-blog-control u-metadata u-text-grey-40 u-metadata-1"><!--blog_post_metadata_date-->
        //                     <span class="u-meta-date u-meta-icon"><!--blog_post_metadata_date_content-->Sat Nov 19 2022<!--/blog_post_metadata_date_content--></span><!--/blog_post_metadata_date--><!--blog_post_metadata_comments-->
        //                     <span class="u-meta-comments u-meta-icon"><!--blog_post_metadata_comments_content-->Comments (0)<!--/blog_post_metadata_comments_content--></span><!--/blog_post_metadata_comments-->
        //                   </div><!--/blog_post_metadata-->
        //                 </div>
        //               </div>
        //                     `
        //                 console.log(tr)
        //                 tbody.appendChild(tr);
        //             }
        //         })
        //     }
        // }

    }
