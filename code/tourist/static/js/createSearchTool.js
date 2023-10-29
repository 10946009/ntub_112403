function autocomplete(inp, arr) {
    var currentFocus; // 紀錄目前焦點所在的索引值
    inp.addEventListener("input", function (e) {
      var a, b, i, val = this.value;
      closeAllLists();
      if (!val) { return false; }
      currentFocus = -1; // 輸入框值變動時重置焦點索引為-1
      a = document.createElement("DIV"); // 建立一個新的DIV元素來放置選項
      a.setAttribute("id", this.id + "autocomplete-list"); // 設定DIV元素的id屬性
      a.setAttribute("class", "create_searchContent"); // 設定DIV元素的class屬性
      this.parentNode.appendChild(a); // 將DIV元素加入輸入框的父元素中

      // 字跟著打在下面框框的部分
      
      b = document.createElement("DIV");
      b.textContent = val; // 輸入的值開頭
      b.innerHTML = `<i class="fas fa-search" style="padding: 10px;"></i><strong>${val}</strong>&emsp;<span style="color:#a1a1a1">-Trip搜尋</span>`;
      b.addEventListener("click", function (e) {
        closeAllLists();
        searchText(val, 'keyword_search');
      });
      a.appendChild(b);

      //隨著元素尋找陣列裡輸入符合的元素
      for (i = 0; i < arr.length; i++) {
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          b = document.createElement("DIV"); // 建立新的DIV元素來放置該項目
          b.innerHTML = `<i class="fas fa-search" style="padding: 10px;cursor: default;"></i><strong>${arr[i].substr(0, val.length)}${arr[i].substr(val.length)}</strong>`;
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>"; // 加入一個隱藏的input元素，用來存放選擇的值
          b.addEventListener("click", function (e) {
            inp.value = this.getElementsByTagName("input")[0].value; // 設定輸入框的值為選擇的值
            closeAllLists(); // 關閉所有項目清單
            searchText(inp.value, 'keyword_search');
          });
          a.appendChild(b); // 將該項目加入清單中

        }
      }
    });



    inp.addEventListener("keydown", function (e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) { // 向下箭頭鍵
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) { // 向上箭頭鍵
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) { // Enter鍵
        e.preventDefault();
        if (currentFocus > -1) { // 如果有選擇項目則觸發點擊事件
          if (x) x[currentFocus].click();
        }
      }
      if (e.key === 'Enter') {//用enter傳送
        e.preventDefault(); // 阻止 Enter本來換行行為
        searchText(inp.value, 'keyword_search');
      }
    });

    function addActive(x) { // 添加選擇時的樣式
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) { // 移除選擇時的樣式
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }

    function closeAllLists(elmnt) { // 關閉所有項目清單
      var x = document.getElementsByClassName("create_searchContent");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) { // 排除目前選擇的項目清單和輸入框本身
          x[i].parentNode.removeChild(x[i]); // 移除該項目清單
        }
      }
    }

    document.addEventListener("click", function (e) {
      closeAllLists(e.target);
    });
  }

    //歷史紀錄（點一下input跳出來）
    const create_searchInput = document.getElementById("create_myInput");
    const create_searchBox = document.getElementById("create_searchBox");
    const create_enter = document.getElementById("create_enter");

    //點不是input裡的元素就關起來
    document.addEventListener("click", function (event) {
        if (!create_searchBox.contains(event.target)) {
            create_searchBox.style.display = "none";
        }
    });

    // 如果input裡有東西的話就關起來，沒有就打開歷史紀錄畫面
    create_searchInput.addEventListener("input", function () {
        const inputValue = create_myInput.value;
        if (inputValue.trim() !== "") {
            create_searchBox.style.display = "none";
        } else {
            create_searchBox.style.display = "block";
        }
    });

    // 點一下input內框跳出來歷史紀錄畫面
    create_searchInput.addEventListener("click", function (event) {
        event.stopPropagation();// 防止觸發 document 上的點擊事件
        create_searchBox.style.display = "block";
    });

    //delete歷史紀錄
    function deleteFunction(element) {
        var historyElement = element.closest('.history_1');
        if (historyElement) {
            historyElement.remove(); //連同父元素删除
        }
    }

// 用來刷新搜尋結果的function
function searchText(search_text, data_type) {
  // data_type= keyword_search,tag_search,popular_search
  console.log(search_text, data_type);

  $.ajax({
      url: '/search/get',  // 伺服器端的 URL
      type: 'GET',  // 請求類型為 GET
      data: {
          search_text: search_text,  // 傳遞給伺服器的參數，以 a_id 為名
          data_type: data_type,
      },
      success: function (response) {
        console.log(response);
          const search_detail_div = $('#replaceable-content');
          search_detail_div.html(response['search_list']);
      },
      error: function (xhr, status, error) {
          // 請求失敗時的處理
          console.log("search_textAJAX請求失敗: " + error);
      }
  });
}