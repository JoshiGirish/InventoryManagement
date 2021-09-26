/*
    This code is used to create pdf of the sales invoice when the user clicks on
    the print button in the display sales orders view
*/

function printInvoice(tag){
    console.log(tag)
    var so_id = tag.dataset.so_id;
    console.log(so_id)
    console.log(tag.dataset.print_url)
    $.ajax({
        url: tag.dataset.print_url,
        data: {
            'so_id': so_id
        },
        dataType:'json',
        success: function(data){
          generatePDF(data);
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

function generatePDF(data){
    console.log(data)
    var faker = window.faker
    // Returns header rows for the main table
    function headRows() {
      return [
        { no: 'No', product: 'Product', quantity: 'Quantity', rate: 'Rate', cgst: 'CGST', sgst:'SGST', igst:'IGST',amount:'Amount' },
      ]
    }
    // Returns body rows for the main table
    function bodyRows(pses) {
      // rowCount = rowCount || 10
      rowCount = pses.length;
      let body = [];
      for (var j = 0; j < rowCount; j++) {
        console.log(pses[j])
        if(pses[j].product==null){
          var product = '--- Deleted Product ---';
        }
        else{
          var product = pses[j].product.name+'\n'+pses[j].product.description;
          console.log(product)
        }
        var p = pses[j].price;
        var q = pses[j].quantity;
        var d = pses[j].discount;
        var amt = (p*q)-(p*q*d/100);
        body.push({
          no: j+1,
          product: product,
          quantity: pses[j].quantity,
          rate: String(Math.round((pses[j].price * 100) / 100).toFixed(2)),
          cgst: String(Math.round((0 * 100) / 100).toFixed(2)),
          sgst: String(Math.round((0 * 100) / 100).toFixed(2)),
          igst: String(Math.round((0 * 100) / 100).toFixed(2)),
          amount: String(Math.round((amt * 100) / 100).toFixed(2))
        })
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
  var doc = new window.jspdf.jsPDF({ orientation: 'portrait', unit: 'mm', lineHeight:1.25, format:'a4' });

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
    
    str = "Sales Order Number";
    doc.setFontSize(12);
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+5;
    
    str = String(data.so.so);
    doc.setFontSize(15);
    doc.text(str, pageWidth-margins.right, atLine,'right');
    atLine += lineHeight+2;
    
    str = "Date: "+ moment(data.so.date).format('MMMM Do YYYY');
    doc.setFontSize(9);
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+2;
    
    str = "Shipping Date: "+ moment(data.so.date).format('MMMM Do YYYY');
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+2;
    
    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight+4;
    
    var part = usableWidth/3;
    doc.setFontSize(12)
      
    var h = [[data.company.name]]
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: 55,
      styles: { cellPadding: 0.5, fontSize: 10},
      head: h,
      headStyles: { fontSize:12 },
      body: [
        [data.company.owner+'\n'+data.company.address],
        [data.company.location],
        [data.company.phone],
        [data.company.email]
      ]
    })

    var h = [['Consumer']]
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: 55,
      styles: { cellPadding: 0.5, fontSize: 10},
      margin: { left: margins.left+part },
      head: h,
      headStyles: { fontSize:12 },
      body: [
        [data.so.consumer.name+'\n'+data.so.consumer.address],
        [data.so.consumer.location],
        [data.so.consumer.phone],
        [data.so.consumer.email]
      ]
    })

    var h = [['Ship To']]
    doc.autoTable({
      startY: atLine-3,
      theme: 'plain',
      tableWidth: 55,
      styles: { cellPadding: 0.5, fontSize: 10},
      margin: { left: margins.left+2*part },
      head: h,
      headStyles: { fontSize:12 },
      body: [
        [data.shippingaddress.name+'\n'+data.shippingaddress.address],
        [data.shippingaddress.location],
        [data.shippingaddress.phone],
        [data.shippingaddress.email]
      ]
    })

    atLine += lineHeight+30;    

    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight;
    
    ///////////////MAIN TABLE///////////////////

      let head = headRows()
      let body = bodyRows(data.so.pses)
      
      doc.autoTable({
        theme: 'plain',
        head: head,
        body: body,
        styles: { fontSize: 10},
        startY: doc.previousAutoTable.finalY + 9,
        rowPageBreak: 'auto',
        bodyStyles: { valign: 'top' },
        didParseCell: function (cell, data) {
                          alignCol(cell, data);
                      }
      })

    var start = margins.left;

    atLine = 220;

    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight+3;
    
    atLine += lineHeight;
    
    // Divider line
    doc.line(margins.left,atLine,pageWidth-margins.right,atLine)
    atLine += lineHeight+4;
    
    str = "Authorized Signatory";
    doc.setFontSize(12);
    doc.text(str, start, atLine+2);
    
    str = "SUB TOTAL :";
    doc.setFontSize(10);
    doc.text(str, pageWidth-margins.right-40, atLine+2,'right');
    str = String(Math.round((data.so.subtotal * 100) / 100).toFixed(2));
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+3;
    
    str = "TAX AMOUNT :";
    doc.text(str, pageWidth-margins.right-40, atLine+2,'right');
    str = String(Math.round((data.so.taxtotal * 100) / 100).toFixed(2));
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+3;
    
    str = "ROUNDED OFF :";
    doc.text(str, pageWidth-margins.right-40, atLine+2,'right');
    str = String(Math.round((data.so.ordertotal * 100) / 100).toFixed(2));
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+3;
    
    str = "ORDER TOTAL :";
    doc.text(str, pageWidth-margins.right-40, atLine+2,'right');
    str = String(Math.round((data.so.ordertotal * 100) / 100).toFixed(2));
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+10;
    
    str = toTitleCase(numWords(Math.round(data.so.ordertotal)));
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+3;
    
    str = "Only";
    doc.text(str, pageWidth-margins.right, atLine+2,'right');
    atLine += lineHeight+5;
    
    str = "NOTE";
    doc.text(str, start, atLine+2);
    atLine += lineHeight+3;
    
    str = "Please deliver in 14 days maximum.";
    doc.text(str, start, atLine+2);
    atLine += lineHeight+3;
    
    var img = new Image()
    img.src = data.company.image
    console.log(img.src)
    img.onload = function(){
              var imageHeightInPdf = 20;
              doc.addImage(img, 'png', margins.left, margins.top, this.width*imageHeightInPdf/this.height, imageHeightInPdf)
              doc.output('dataurlnewwindow');
              // doc.save("C:/Users/Girish/Desktop/jspdf/example.pdf");
              }

    };