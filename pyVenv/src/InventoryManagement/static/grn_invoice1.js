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
    var grn = data.grn;
    var grnes = data.grnes;
    console.log(data);
    var faker = window.faker;
    sumReceived = 0;
    sumAccepted = 0;
    sumRejected = 0;
      
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

    
    
    ///////////////MAIN TABLE///////////////////

      let head = headRows()
      let body = bodyRows(data.grn.grnes)

      // Push totals in the last row
      body.push(['','','Total',sumReceived,sumAccepted,sumRejected,''])
      part = usableWidth/4;

      doc.autoTable({
        theme: 'striped',
        head: head,
        body: body,
        styles: { fontSize: 10},
        startY: doc.previousAutoTable.finalY + 9,
        pageBreak: 'auto',
        // rowPageBreak: 'auto',
        bodyStyles: { valign: 'top' },
        didParseCell: function (cell, data) {
                          alignCol(cell, data);
                      },
        didDrawPage: function (hookdata) {
          // Header
                  // Company logo
              var img = new Image()
              img.src = data.company.image
              console.log(img.src)
              img.onload = function(){
                        var imageHeightInPdf = 20;
                        doc.addImage(img, 'png', margins.left, margins.top, this.width*imageHeightInPdf/this.height, imageHeightInPdf)
                        doc.output('dataurlnewwindow');
                        // doc.save("C:/Users/Girish/Desktop/jspdf/example.pdf");
                        }

                doc.autoTable({
                  startY: margins.top,
                  theme: 'plain',
                  tableWidth: part,
                  styles: { cellPadding: 0.5, fontSize: 10},
                  margin: { left: 3*usableWidth/4 },
                  bodyStyles:{halign:'right'},
                  body: [
                    ["Original for Recepient"],
                    ["Goods Receipt Note"],
                    [String(data.grn.identifier)],
                    ["Date: "+ moment(data.grn.date).format('MMMM Do YYYY')]
                  ]
                })

              
              // Divider line
              doc.line(margins.left,40,pageWidth-margins.right,40)
              
                
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
                startY: margins.top+30,
                theme: 'plain',
                tableWidth: part*2,
                styles: { cellPadding: 0.5, fontSize: 10},
                headStyles: { fontSize:12 },
                body: grn_body,
                columnStyles: {
                  0: {cellWidth: 2*part/3}, // Less width for first column
                  1: {cellWidth: 4*part/3},}
              })

              
              doc.autoTable({
                startY: margins.top+30,
                theme: 'plain',
                tableWidth: part,
                styles: { cellPadding: 0.5, fontSize: 10},
                head: [[data.company.name]],
                margin: { left: margins.left+2*part },
                headStyles: { fontSize:12 },
                body: [
                  [data.company.owner+'\n'+data.company.address],
                  [data.company.location],
                  [data.company.phone],
                  [data.company.email]
                ]
              })

              
              doc.autoTable({
                startY: margins.top+30,
                theme: 'plain',
                tableWidth: part,
                styles: { cellPadding: 0.5, fontSize: 10},
                margin: { left: margins.left+3*part },
                head: [['Vendor']],
                headStyles: { fontSize:12 },
                body: [
                  [data.grn.vendor.name+'\n'+data.grn.vendor.address.name+'\n'+data.grn.vendor.address.address],
                  [data.grn.vendor.address.city],
                  [data.communication.phone],
                  [data.communication.email]
                ]
              })


              // Divider line
              doc.line(margins.left,155,pageWidth-margins.right,155)


          // Footer
              var start = margins.left;
              // var h = [['Prepared By']]
              doc.autoTable({
                startY: 160,
                theme: 'grid',
                tableWidth: usableWidth/4,
                styles: { cellPadding: 0.5, fontSize: 10},
                margin: { left: margins.left},
                // head: h,
                bodyStyles: { valign: 'top', halign: 'center'},
                headStyles: { fontSize:10, halign: 'center'},
                rowStyles: {
                  0: {rowHeight: 12},
                  1: {rowHeight: 30}
                },
                body: [
                      ["Prepared By\n(Stores' Asst.)","Checked By\n(Stores' Incharge)","Inspected By\n(Quality Incharge)",'Approved By\n(Plant Head)'],
                      ["\n\n","\n\n","\n\n","\n\n"]
                    ]
                  })
        }
      })
  };
  