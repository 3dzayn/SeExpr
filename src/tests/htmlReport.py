#!/usr/bin/python

import sys
import os

if len(sys.argv)==2:
    filenameIn=sys.argv[1]
else:
    print "    usage: htmlReport <CSV_filename>"
    sys.exit(0)

tbl="""<html>
<head>
<style>
body {font-family: Arial, sans-serif;}
td {width: 100pt;}
td.medium {background: orange;}
td.bad {background: red;}
td.good {background: green;}
td.broke {background: black;}
tr:nth-child(even) {background: #CCC}
tr:nth-child(odd) {background: #FFF}
tr.head {background:#333333;color:#eeeeee;}
td.neutral {} 
.sorty{
	float:right;
    display:block;
    width:0; height:0;
    border-left: 5px solid black;
    border-right: 5px solid black;
    border-bottom: 5px solid black;
    border-color: #eeeeee;
    margin:5px;
}
.upArrow{
    float:right;
    display:block;
    width:0; height:0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 5px solid black;
    border-color: #eeeeee;
    margin:5px;
}
.downArrow{
    display:block;
    float:right;
    width:0; height:0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid black;
    border-color: #eeeeee;
    margin:5px;
}
</style>
</head>
<body>

<script>
	function sortTable(table,col,reverse){
		var body=table.tBodies[0];
		var tr=Array.prototype.slice.call(body.rows,0);
		if(reverse==0) reverse=-1;
		tr=tr.sort(function(a,b){
			if(col == 0) return -reverse*a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim());
			var anum=parseFloat(a.cells[col].textContent)
			var bnum=parseFloat(b.cells[col].textContent);
			return -reverse*(anum-bnum);

			//return reverse*a.cells[col].textContent.trim().localeCompare(b.cells[col].textContent.trim());

		});
		for(var i=0;i<tr.length;i++) body.appendChild(tr[i]);
	}
	function makeSortable(table) {
	    var th = table.tHead;
	    if(th){
	    	var thRows=th.rows[0];
	    	if(thRows){
	    		var thRowsCells=thRows.cells;
	    		if(thRowsCells){
		    		for(var i=0;i<thRowsCells.length;i++){
		    			var sorterClosure=function ( ii){
					        var dir = 1;
					        var spans=thRowsCells[i].getElementsByTagName("span")[0];
					        thRowsCells[ii].addEventListener('click', function () {
						        //spans.innerHTML=dir;
						        for(var j=0;j<thRowsCells.length;j++){
							        var spans2=thRowsCells[j].getElementsByTagName("span")[0];
						    		spans2.className="sorty";
						        }
					        	spans.className=dir ? "upArrow" : "downArrow";
					            sortTable(table, ii, (dir = 1 - dir))
					        });
					    };
					    sorterClosure(i);
				    }
				}
	    	}
	    }
	}

	var done;
	window.onload=function(){
		done=1;
		var tables=document.body.getElementsByTagName("table");
		for(var i=0;i<tables.length;i++){
			makeSortable(tables[i]);
		}
	}
</script>
"""

def getFloat(val):
	return float(val.split(" ")[0])
def percentToStyle(percent):
	if percent<-5:
		return "bad"
	elif percent <5:
		return "medium"
	else:
		return "good"

try:
    csvData=open(filenameIn)
except:
    print "File " + filenameIn + " doesn't exist"
    sys.exit(1)

lines=csvData.readlines()
tbl+="<table>\n"
lines.insert(0,"Test,V1,V2 interpreter,V2 interpreter percent,V2 llvm,V2 llvm percent")

tbl+="<thead>"
items=lines[0].split(",")
tbl+="<tr class='head'>\n"+"".join(["    <td><span class='sorty'></span>"+x+"</td>\n" for x in items])+"</tr>"
tbl+="</thead>"
tbl+="<tbody>"

for line in lines[1:]:
	items=line.split(",")
	v1=getFloat(items[1])
	v2interpreter=getFloat(items[2])
	v2llvm=getFloat(items[3])

	styles=["label","","broke","broke","broke","broke"]
	items[1]="%.1f ms"%v1
	if v2interpreter != -1:
		styles[2]=""
		items[2]="%.1f ms"%v2interpreter
		percent=(v1-v2interpreter)/v1*100
		items[3]="%.0f%%"%percent
		styles[3]=percentToStyle(percent)
	items.append("")
	items.append("")
	if v2llvm != -1:
		styles[4]=""
		items[4]="%.1f ms"%v2llvm
		percent=(v1-v2llvm)/v1*100
		items[5]="%.0f%%"%percent
		styles[5]=percentToStyle(percent)
	s="<tr>"+"".join(["<td class='%s'>%s</td>\n"%xs for xs in zip(styles,items)])+"</tr>"
	tbl+=s
tbl+="</tbody>"
tbl+="</table>\n"
tbl+="</body></html>"
open("test.html","w").write(tbl)
