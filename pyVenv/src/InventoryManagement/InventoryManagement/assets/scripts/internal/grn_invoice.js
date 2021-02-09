/*
    This code is used to create pdf of the goods receipt note when the user clicks on
    the print button in the display purchase orders view
*/

function printGRNInvoice(tag){
    console.log(tag)
    var grn_id = tag.dataset.grn_id;
    console.log(grn_id)
    console.log(tag.dataset.print_url)
    $.ajax({
        url: tag.dataset.print_url,
        data: {
            'grn_id': grn_id
        },
        dataType:'json',
        success: function(data){
          var imgURL = data.company.image;
          console.log(data.company.image);
          convertImageAndGeneratePDF(imgURL,data);
          }
    });
};


// Convert order amount to words
const a = ['', 'one ', 'two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 'eight ', 'nine ', 'ten ', 'eleven ', 'twelve ', 'thirteen ', 'fourteen ', 'fifteen ', 'sixteen ', 'seventeen ', 'eighteen ', 'nineteen ']
const b = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

const regex = /^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/

function numWords (num) {
  if ((num = num.toString()).length > 9) {
    throw new Error('overflow') // Does not support converting more than 9 digits yet
  }

  const n = ('000000000' + num).substr(-9).match(regex)
  if (!n) return

  let str = ''
  str += (n[1] != 0) ? (a[Number(n[1])] || b[n[1][0]] + ' ' + a[n[1][1]]) + 'crore ' : ''
  str += (n[2] != 0) ? (a[Number(n[2])] || b[n[2][0]] + ' ' + a[n[2][1]]) + 'lakh ' : ''
  str += (n[3] != 0) ? (a[Number(n[3])] || b[n[3][0]] + ' ' + a[n[3][1]]) + 'thousand ' : ''
  str += (n[4] != 0) ? (a[Number(n[4])] || b[n[4][0]] + ' ' + a[n[4][1]]) + 'hundred ' : ''
  str += (n[5] != 0) ? ((str != '') ? 'and ' : '') + (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) : ''

  return str.trim()
}

// To capital case
function toTitleCase(aString) {
  return aString.replace(/(?:^|\s)\w/g, function(match) {
      return match.toUpperCase();
  });
}


//////////// Computing data url for image of company logo //////////////
var convertImageAndGeneratePDF = function(url, data) {
  var img = new Image, data, ret={imgdata: null, pending: true};
  
  img.onError = function() {
    throw new Error('Cannot load image: "'+url+'"');
  }
  img.onload = function() {
    var canvas = document.createElement('canvas');
    document.body.appendChild(canvas);
    canvas.width = img.width;
    canvas.height = img.height;
    
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    // Grab the image as a jpeg encoded in base64, but only the data
    imgdata = canvas.toDataURL('image/jpeg').slice('data:image/jpeg;base64,'.length);
    // Convert the data to binary form
    imgdata = atob(imgdata)
    document.body.removeChild(canvas);
    
    ret['data'] = imgdata;
    ret['pending'] = false;
    generatePDF(data,imgdata);
  }
  img.src = url;
}



function generatePDF(data,imgdata){
    var grn = data.grn;
    var grnes = data.grnes;
    console.log(data);
    var faker = window.faker;
    sumReceived = 0;
    sumAccepted = 0;
    sumRejected = 0;
    var numPages = 0;

    // Returns header rows for the main table
    function headRows() {
      return [
        { no: 'No', product: 'Product', po: 'PO', received: 'Received', accepted: 'Accepted', rejected:'Rejected', remark:'Remarks'},
      ]
    }
    // Returns body rows for the main table
    function bodyRows(grnes) {
      // rowCount = rowCount || 10
      rowCount = grnes.length;
      let body = [];
      for (var j = 0; j < rowCount; j++) {
        console.log(grnes[j])
        if(grnes[j].product==null){
          var product = '--- Deleted Product ---';
        }
        else{
          var product = grnes[j].product.name+'\n'+grnes[j].product.description;
          console.log(product)
        }
        var p = grnes[j].price;
        var q = grnes[j].quantity;
        var d = grnes[j].discount;
        var amt = (p*q)-(p*q*d/100);
        body.push({
          no: j+1,
          product: product,
          po: grnes[j].po_id,
          received: grnes[j].receivedQty,
          accepted: grnes[j].acceptedQty,
          rejected: grnes[j].rejectedQty,
          remark: grnes[j].remark,
        })

        // Calculate totals
        sumReceived += grnes[j].receivedQty;
        sumAccepted += grnes[j].acceptedQty;
        sumRejected += grnes[j].rejectedQty;
      }
      return body
    }

    // Aligns to right, the monetary columns in main table
    function alignCol(data){
      var col = data.column.index;
      if(col>1){
          data.cell.styles.halign = 'right';
        }
    }

  // Don't forget, that there are CORS-Restrictions. So if you want to run it without a Server in your Browser you need to transform the image to a dataURL
  // Use http://dataurl.net/#dataurlmaker
  var doc = new jsPDF({ orientation: 'landscape', unit: 'mm', lineHeight:1.25, format:'a4' });

  doc.addFont('Verdana', 'Arial', 'normal');
  doc.setFont('Verdana');

  margins = {
              top: 15,
              bottom: 15,
              left: 15,
              right: 15
          };
    var lineHeight = 3;
    var atLine = margins.top;
    var pageHeight = doc.internal.pageSize.height || doc.internal.pageSize.getHeight();
    var pageWidth = doc.internal.pageSize.width || doc.internal.pageSize.getWidth();
    var usableWidth = pageWidth-margins.left-margins.right;

    // Company logo
    // var img = new Image()
    // img.src = data.company.image
    // console.log(img.src)
    // img.onload = function(){
    //           var imageHeightInPdf = 20;
    //           doc.addImage(img, 'png', margins.left, margins.top, this.width*imageHeightInPdf/this.height, imageHeightInPdf)
    //   // doc.save("C:/Users/Girish/Desktop/jspdf/example.pdf");
    //   }

    let str = "Original for Recepient";
    doc.setFontSize(9);
    doc.text(str, pageWidth-margins.right, atLine,'right');
    atLine += lineHeight;
    
    str = "Goods Receipt Note";
    doc.setFontSize(12);
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+5;
    
    str = String(data.grn.identifier);
    doc.setFontSize(15);
    doc.text(str, pageWidth-margins.right, atLine,'right');
    atLine += lineHeight+2;
    
    str = "Date: "+ moment(data.grn.date).format('MMMM Do YYYY');
    doc.setFontSize(9);
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+2;
    
    // str = "Shipping Date: "+ moment(data.grn.date).format('MMMM Do YYYY');
    // doc.text(str, pageWidth-margins.right, atLine+2,'right');
    // atLine += lineHeight+2;
    
    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight+4;
    
    var part = usableWidth/4;
    doc.setFontSize(12)
      
    ///////////////GRN DETAILS TABLE///////////////////

    // let head = headRows()
    let grn_body = []
    grn_fields_with_poRef = ['identifier','grnType','date','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber']
    grn_body.push(
      ['PO', ':' + grn.identifier],
      ['Receipt Type',':' + (grn.grnType=='auto') ? 'GRN with PO reference' : 'GRN without PO reference'],
      ['Date',':' + grn.date],
      ['Amendment Number', ':' + grn.amendNumber],
      ['Amendment Date', ':' + grn.amendDate],
      ['Transporter', ':' + grn.transporter],
      ['Vehicle Number', ':' + grn.vehicleNumber],
      ['Inward Number', ':' + grn.gateInwardNumber]) 
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: part*2,
      styles: { cellPadding: 0.5, fontSize: 10},
      head: h,
      headStyles: { fontSize:12 },
      body: grn_body,
      columnStyles: {
        0: {cellWidth: 2*part/3}, // Less width for first column
        1: {cellWidth: 4*part/3},}
    })

    var h = [[data.company.name]]
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: part,
      styles: { cellPadding: 0.5, fontSize: 10},
      head: h,
      margin: { left: margins.left+2*part },
      headStyles: { fontSize:12 },
      body: [
        [data.company.owner+'\n'+data.company.address],
        [data.company.location],
        [data.company.phone],
        [data.company.email]
      ]
    })

    var h = [['Vendor']]
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: part,
      styles: { cellPadding: 0.5, fontSize: 10},
      margin: { left: margins.left+3*part },
      head: h,
      headStyles: { fontSize:12 },
      body: [
        [data.grn.vendor.name+'\n'+data.grn.vendor.address.name+'\n'+data.grn.vendor.address.address],
        [data.grn.vendor.address.city],
        [data.communication.phone],
        [data.communication.email]
      ]
    })


    atLine += lineHeight+35;    

    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight;
    
    ///////////////MAIN TABLE///////////////////

      let head = headRows()
      let body = bodyRows(data.grn.grnes)

      // Push totals in the last row
      body.push(['','','Total',sumReceived,sumAccepted,sumRejected,''])
      var mainTableMargins = {
              top: 85,
              bottom: 40,
              left: 15,
              right: 15
      }

      doc.autoTable({
        theme: 'striped',
        head: head,
        body: body,
        styles: { fontSize: 10},
        startY: 85,
        margin: mainTableMargins,
        rowPageBreak: 'auto',
        bodyStyles: { valign: 'top' },
        didParseCell: function(celldata){
                          alignCol(celldata)
                      },
        willDrawCell: function (hookdata) {
                          // var hgt = 0;
                          // var all = data.table.allRows();
                          // for (var rowIndex = 0; rowIndex < all.length; rowIndex++) {
                          //     var row = all[rowIndex];
                          //     hgt += row.height;
                          // }
                          // console.log(hgt);
                          console.log(hookdata.cell.height);
                      },
        didDrawPage: function (hookdata){
          numPages += 1;
          ////////////////// HEADER ////////////////////

          /////////// COMPANY LOGO ////////////////////
          var imageHeightInPdf = 20;
          doc.addImage(imgdata, 'JPEG', margins.left, margins.top, this.width*imageHeightInPdf/this.height, imageHeightInPdf) 

          margins = {
                      top: 15,
                      bottom: 15,
                      left: 15,
                      right: 15
                  };
          var lineHeight = 3;
          var atLine = margins.top;
          var pageHeight = doc.internal.pageSize.height || doc.internal.pageSize.getHeight();
          var pageWidth = doc.internal.pageSize.width || doc.internal.pageSize.getWidth();
          var usableWidth = pageWidth-margins.left-margins.right;
          let str = "Original for Recepient";
          doc.setFontSize(9);
          doc.text(str, pageWidth-margins.right, atLine,'right');
          atLine += lineHeight;
          
          str = "Goods Receipt Note";
          doc.setFontSize(12);
          doc.text(str, pageWidth-margins.right, atLine+2,'right');
          atLine += lineHeight+5;
          
          str = String(data.grn.identifier);
          doc.setFontSize(15);
          doc.text(str, pageWidth-margins.right, atLine,'right');
          atLine += lineHeight+2;
          
          str = "Date: "+ moment(data.grn.date).format('MMMM Do YYYY');
          doc.setFontSize(9);
          doc.text(str, pageWidth-margins.right, atLine+2,'right');
          atLine += lineHeight+2;
          
          // str = "Shipping Date: "+ moment(data.grn.date).format('MMMM Do YYYY');
          // doc.text(str, pageWidth-margins.right, atLine+2,'right');
          // atLine += lineHeight+2;
          
          // Divider line
          doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
          atLine += lineHeight+4;
          
          var part = usableWidth/4;
          doc.setFontSize(12)
            
          ///////////////GRN DETAILS TABLE///////////////////
      
          // let head = headRows()
          let grn_body = []
          grn_fields_with_poRef = ['identifier','grnType','date','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber']
          grn_body.push(
            ['GRN', ':' + grn.identifier],
            ['Receipt Type',':' + (grn.grnType=='auto') ? 'GRN with PO reference' : 'GRN without PO reference'],
            ['Date',':' + grn.date],
            ['Amendment Number', ':' + grn.amendNumber],
            ['Amendment Date', ':' + grn.amendDate],
            ['Transporter', ':' + grn.transporter],
            ['Vehicle Number', ':' + grn.vehicleNumber],
            ['Inward Number', ':' + grn.gateInwardNumber]) 
          doc.autoTable({
            startY: atLine-3,
            theme: 'plain',
            tableWidth: part*2,
            styles: { cellPadding: 0.5, fontSize: 10},
            head: h,
            headStyles: { fontSize:12 },
            body: grn_body,
            columnStyles: {
              0: {cellWidth: 2*part/3}, // Less width for first column
              1: {cellWidth: 4*part/3},}
          })
      
          var h = [[data.company.name]]
          doc.autoTable({
            startY: atLine-3,
            theme: 'plain',
            tableWidth: part,
            styles: { cellPadding: 0.5, fontSize: 10},
            head: h,
            margin: { left: margins.left+2*part },
            headStyles: { fontSize:12 },
            body: [
              [data.company.owner+'\n'+data.company.address],
              [data.company.location],
              [data.company.phone],
              [data.company.email]
            ]
          })
      
          var h = [['Vendor']]
          doc.autoTable({
            startY: atLine-3,
            theme: 'plain',
            tableWidth: part,
            styles: { cellPadding: 0.5, fontSize: 10},
            margin: { left: margins.left+3*part },
            head: h,
            headStyles: { fontSize:12 },
            body: [
              [data.grn.vendor.name+'\n'+data.grn.vendor.address.name+'\n'+data.grn.vendor.address.address],
              [data.grn.vendor.address.city],
              [data.communication.phone],
              [data.communication.email]
            ]
          })
      
      
          atLine += lineHeight+35;    
      
          // Divider line
          doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
          atLine += lineHeight;

          var start = margins.left;


          //////////////// FOOTER /////////////////
            part = usableWidth/4;
            // var h = [['Prepared By']]
            doc.autoTable({
              startY: 170,
              theme: 'grid',
              tableWidth: part,
              styles: { cellPadding: 0.5, fontSize: 10},
              margin: { left: margins.left},
              // head: h,
              bodyStyles: { valign: 'top', halign: 'center'},
              headStyles: { fontSize:10, halign: 'center', fillColor:[240, 240, 240],textColor:0,fontStyle:'normal'},
              rowStyles: {
                0: {rowHeight: 12},
                1: {rowHeight: 30}
              },
              head:[{
                      prepared:"Prepared By\n(Stores' Asst.)",
                      checked:"Checked By\n(Stores' Incharge)",
                      inspected:"Inspected By\n(Quality Incharge)",
                      approved:"Approved By\n(Plant Head)"}],
              body: [{
                      prepared:'\n\n',
                      checked:'\n\n',
                      inspected:'\n\n',
                      approved:'\n\n'}],
              columnStyles: {
                0: {cellWidth: usableWidth/4}, // Less width for first column
                1: {cellWidth: usableWidth/4},
                2: {cellWidth: usableWidth/4},
                3: {cellWidth: usableWidth/4}
              }
            })
          }
        })

      
      // Company logo
      var img = new Image()
      img.src = data.company.image
      console.log(img.src)
      img.onload = function(){
                var imageHeightInPdf = 20;
                for(var i=1; i<=numPages;i++){
                  doc.setPage(i);
                  doc.addImage(img, 'PNG', margins.left, margins.top, this.width*imageHeightInPdf/this.height, imageHeightInPdf);

                  // Add page number in the footer
                  var str = 'Page ' + i;
                  str = str + ' of ' + numPages;
                  doc.setFontSize(10);

                  // doc.text(str, margins.left, pageHeight - 10);
                  doc.text(str, pageWidth-margins.right, pageHeight - 10,'right');
                }
        // doc.save("C:/Users/Girish/Desktop/jspdf/example.pdf");
        doc.output('dataurlnewwindow');
        }
      
    // doc.text(str, start, atLine);
    // atLine += lineHeight+3+20;
    
    // str = "Please deliver in 14 days maximum.";
    // doc.text(str, start, atLine+2);
    // atLine += lineHeight+3;

  };