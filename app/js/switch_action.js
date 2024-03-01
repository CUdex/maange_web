function toggleCheckbox() {
    const checkbox = event.target;
    const instanceId = checkbox.getAttribute("instance-id");
    const value = checkbox.getAttribute("value") === "enable" ? "disable" : "enable";
    const tagKey = checkbox.getAttribute("tag_key");

    console.log(instanceId, value, tagKey);
    var data = {
        instance_id: instanceId,
        tag_key: tagKey,
        state: value
    };

    // put 요청 보내기
    axios
    .put("/cloud_list/tag", data, {
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(function(response) {
        if (response.status === 200) {
            // 응답이 성공적으로 받아졌을 때 리다이렉션
            alert("태그 업데이트 완료");
        } else {
            // 응답이 실패했을 때 에러 처리
            alert("Failed Update Tag");
        }
    })
    .catch(function(error) {
        // error 처리
        alert("put method error.");
        console.error(error);
    });
}