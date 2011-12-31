var editor;
KindEditor.ready(function(K) {
	editor = K.create('textarea[name="content"]', {
		uploadJson:'/admin/file_upload_json',
		fileManagerJson:'/admin/file_manager_json',
		allowFileManager : true
	});
});