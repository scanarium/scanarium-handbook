function clearClass(node, className) {
    var classList = node.classList;
    if (classList) {
        classList.remove(className);
    }
    if (node.hasChildNodes()) {
        var childNodes = node.childNodes;
        for (let i = 0; i < childNodes.length; i++) {
            clearClass(childNodes[i], className);
        }
    }
}

function scrapeTocObjFromDocument() {
    var parents = [newTocObj(0)];

    function newTocObj(level, id, name) {
        return {
            level: level,
            id: id ? id : null,
            name: name ? name : null,
            subnodes: [],
        };
    };

    function add(tocObj) {
        parents[parents.length - 1].subnodes.push(tocObj);
        parents.push(tocObj);
    };

    const nodes = document.getElementsByClassName('document-generator-node');
    for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        if (node.nodeName.substring(0,1).toUpperCase() == 'H') {
            const level = parseInt(node.nodeName.substring(1), 10)
            const tocObj = newTocObj(level, node.id, node.innerText);

            const expectedParentLevel = level - 1;
            var searching = true;
            var j=0;
            while (searching &&  j < 10) {
                var parentLevel = parents[parents.length - 1].level;
                if (parentLevel + 1 == level) {
                    add(tocObj);
                    searching = false;
                } else if (parentLevel + 1 > level) {
                    parents.pop();
                } else if (parentLevel + 1 < level) {
                    var stub = newTocObj(parentLevel + 1);
                    add(stub);
                }
                j++;
            }
            if (j >= 10) {
                console.log('Logic error when enqueueing', node);
            }
        }
    }
    var tree = parents[0];
    while (tree.id == null && tree.name == null && tree.subnodes.length == 1) {
        tree = tree.subnodes[0];
    }
    return tree;
}

function selectTocListItem(item) {
    var toc = document.getElementById('toc');

    var isFirstSelect = true;
    var previousSelectedItem = toc.tocSelectedItem
    if (previousSelectedItem) {
        previousSelectedItem.querySelector('.toc-label').classList.remove('toc-label-selected');
        isFirstSelect = (item != previousSelectedItem);
    }
    item.querySelector('.toc-label').classList.add('toc-label-selected');
    toc.tocSelectedItem = item;

    classLists = [item.querySelector('.toc-bullet').classList]
    var subnodeList = item.querySelector('ul');
    if (subnodeList) {
        classLists.push(subnodeList.classList);
    }
    if (!item.classList.contains('toc-item-l1')) {
        if (isFirstSelect) {
            classLists.forEach(classList => {
                classList.remove('toc-collapsed');
            });
        } else {
            classLists.forEach(classList => {
                classList.toggle('toc-collapsed');
            });
        }
    }
}

function tocToElement(tocObj) {
    var element = document.createElement('li');
    element.className = 'toc-item-l' + (tocObj.level);

    var label = document.createElement('div');
    label.className = 'toc-label toc-label-l' + (tocObj.level);
    label.onclick = function(e) {
        if (tocObj.level == 1) {
            document.body.classList.toggle('toc-open');
        } else {
            var element = this;
            while (element.nodeName.toUpperCase() != 'LI') {
                element = element.parentElement;
            }
            selectTocListItem(element);
        }
    }

    var bullet = document.createElement('img');
    var classList = bullet.classList;
    classList.add('toc-bullet');
    if (tocObj.level == 1) {
        bullet.src = 'images/toc-bullet-minus.svg';
    } else {
        bullet.src = 'images/toc-bullet-plain.svg';
        if (tocObj.subnodes.length > 0) {
            classList.add('toc-bullet-toggle');
            classList.add('toc-collapsed');
            bullet.src = 'images/toc-bullet-toggle.svg';
        } else {
            classList.add('toc-bullet-plain');
        }
    }
    label.appendChild(bullet);

    var labelText = document.createTextNode(tocObj.name ? tocObj.name : '---');
    label.appendChild(labelText);


    if (tocObj.id != null) {
        var link = document.createElement('a')
        link.className = 'toc-link';
        if (tocObj.level > 1) {
            link.href = '#' + tocObj.id;
        }
        link.appendChild(label);
        label = link;
    }

    element.appendChild(label);

    if (tocObj.subnodes.length > 0) {
        var subelements = document.createElement('ul');
        if (tocObj.level > 1) {
            subelements.className = 'toc-collapsed';
        }
        tocObj.subnodes.forEach(subnode => {
            subelements.appendChild(tocToElement(subnode));
        });

        element.appendChild(subelements);
    }
    return element;
}

function addTableOfContents() {
    var tree = scrapeTocObjFromDocument();

    var toc = document.createElement('ul');
    toc.id = 'toc';
    toc.appendChild(tocToElement(tree));

    var tocContainer = document.createElement('div');
    tocContainer.id = 'toc-container';

    var tocToggle = document.createElement('img');
    tocToggle.id = 'toc-toggle';
    tocToggle.src = 'images/toc-bullet-plus.svg';
    tocToggle.onclick = function() {
        document.body.classList.toggle('toc-open');
    };

    tocContainer.appendChild(tocToggle);


    tocContainer.appendChild(toc);

    document.body.appendChild(tocContainer);
}

document.addEventListener ("DOMContentLoaded", () => {
	addTableOfContents();
});