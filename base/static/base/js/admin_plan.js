var script = document.createElement('script');
script.type = 'text/javascript';

script.onload = function () {
    document.addEventListener("DOMContentLoaded", function () {
        var planField = document.getElementById('id_plan');
        var image4Field = document.getElementById('image4');
        var image5Field = document.getElementById('image5');
        var image6Field = document.getElementById('image6');

        function updateFields() {
            var isPaid = planField.value == 'PAID';
            if (isPaid) {
                if (!image4Field.parentNode) {
                    planField.parentNode.appendChild(image4Field);
                    planField.parentNode.appendChild(image5Field);
                    planField.parentNode.appendChild(image6Field);
                }
            } else {
                if (image4Field.parentNode) {
                    image4Field.remove();
                    image5Field.remove();
                    image6Field.remove();
                }
            }

            planField.addEventListener('change', updateFields);
            updateFields();
        });
};
document.head.appendChild(script);
