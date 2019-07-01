];

function modifyRunningOrder(ro) {

  var new_ro = [];
  item_count=0;
  for (var i in ro) {
    var item = ro[i];
    if (item[0].type.startsWith("rel")|| item[0].type.startsWith("and") || item[0].type.startsWith("adverb")||item[0].type.startsWith("filler")) {
        item_count++;
        new_ro.push(item);
        if (item_count%12===0 & item_count<95){
            if (item_count===84){
                text="End of block. Only 1 block left!";
                }
            else {
                text="End of block. "+(8-(Math.floor(item_count/12)))+" blocks left.";
            }ro[i].push(new DynamicElement("Message", {html: text}));
        }
      } else {
      new_ro.push(item);
      }
  }
  return new_ro;
}
