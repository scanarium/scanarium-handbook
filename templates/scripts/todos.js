function decorateTodos() {
    const nodes = document.getElementsByClassName('todo');
    for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        node.id='todo-' + (i+1);

        var navigation = document.createElement('span');
        if (nodes.length > 1) {
            var link = document.createElement('a');
            link.href = '#todo-' + (i == 0 ? nodes.length : i);
            link.appendChild(document.createTextNode('<<'));
            navigation.appendChild(link);
        }
        navigation.appendChild(document.createTextNode(' #' + (i+1) + ' '));
        if (nodes.length > 1) {
            var link = document.createElement('a');
            link.href = '#todo-' + (i < nodes.length - 1 ? i + 2 : 1);
            link.appendChild(document.createTextNode('>>'));
            navigation.appendChild(link);
        }
        navigation.appendChild(document.createTextNode(' '));

        if (node.hasChildNodes()) {
            node.insertBefore(navigation, node.firstChild);
        } else {
            node.appendChild(navigation);
        }
    }
    if (nodes.length > 0) {
        var node = document.createElement('p');
        node.className = 'todo'

        var link = document.createElement('a');
        link.href = '#todo-1';
        link.appendChild(document.createTextNode('There are ' + (nodes.length) + ' todos in this document'));

        node.appendChild(link);

        var parent = document.getElementById('content');
        parent.insertBefore(node, parent.firstChild);

        document.title = '(' + (nodes.length - 1) + ') ' + document.title;
    }
}

document.addEventListener ("DOMContentLoaded", () => {
    decorateTodos();
});
