var script = document.createElement('script');
script.type = 'text/javascript';
script.referrerPolicy = "origin";
script.src = "https://cdn.tiny.cloud/1/scsoshxtg5srh8ink8hkauqc7jvjkiy4wsumjskawis3ic9u/tinymce/7/tinymce.min.js";

script.onload = function () {
    document.addEventListener("DOMContentLoaded", function () {
        var element = document.querySelector(".border.break-words.font-medium.invisible.max-w-4xl.px-3.py-2.text-sm");
        if (element) {
            element.style.minHeight = "0";
        }
        tinymce.init({
            selector: "#id_description",
            height: 656,
            plugins: [
                'advlist autolink link image lists charmap print preview hr anchor pagebreak',
                'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
                'table emoticons template paste help',
                'codesample',
                'link',
                'image',
                'code',
                'table',
                'lists',
                'media'
            ],
            toolbar: 'undo redo | formatselect | bold italic underline strikethrough | ' +
                'fontselect fontsizeselect | alignleft aligncenter alignright alignjustify | ' +
                'outdent indent | numlist bullist checklist | forecolor backcolor removeformat | ' +
                'pagebreak | charmap emoticons | fullscreen preview save print | insertfile image media template link anchor codesample | ' +
                'link image code table lists media | help',
            menubar: 'file edit view insert format tools table help',
            toolbar_drawer: 'floating',
            tinycomments_mode: 'embedded',
            tinycomments_author: 'Author name',
        });
    });
}
document.head.appendChild(script);
