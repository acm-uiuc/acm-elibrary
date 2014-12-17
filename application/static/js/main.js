var options = {
  // valueNames: [ 'title', 'description' ]
  valueNames: [ 'title' ]
};
var docList;

$(function() {
    $(document).foundation();
    docList = new List('docs', options);
});
