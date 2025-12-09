(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const cat = document.getElementById('id_categoria');
        const sub = document.getElementById('id_subcategoria');
        if (!cat || !sub) return;

        let mapping = {};
        try {
            mapping = cat.dataset.submap ? JSON.parse(cat.dataset.submap) : {};
        } catch (e) {
            mapping = {};
        }

        function rebuild() {
            const current = sub.value;
            const opts = mapping[cat.value] || [];
            sub.innerHTML = '';
            const blank = document.createElement('option');
            blank.value = '';
            blank.textContent = '---------';
            sub.appendChild(blank);
            opts.forEach(function(item) {
                const [val, label] = item;
                const opt = document.createElement('option');
                opt.value = val;
                opt.textContent = label;
                if (val === current) opt.selected = true;
                sub.appendChild(opt);
            });
        }

        cat.addEventListener('change', rebuild);
        rebuild();
    });
})();






