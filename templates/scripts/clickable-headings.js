function makeHeadingClickable(node) {
    var link = document.createElement('a');
    link.href = '#' + node.id;
    link.className = 'clickable-heading-link';

    while (node.firstChild) {
      var child = node.firstChild;
      node.removeChild(child);
      link.appendChild(child);
    }

    node.appendChild(link);
}

function makeHeadingsClickable() {
    const nodes = document.getElementsByClassName('document-generator-node');
    for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        if (node.nodeName.substring(0,1).toUpperCase() == 'H') {
            const level = parseInt(node.nodeName.substring(1), 10)
            if (level >= 1) {
                makeHeadingClickable(node);
            }
        }
    }
}

document.addEventListener ("DOMContentLoaded", () => {
	makeHeadingsClickable();
});
