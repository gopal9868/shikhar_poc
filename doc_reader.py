import pdfplumber
import fitz
def extract_box_content(pdf_path, page_number, box_coords):
    """
    Extract text content from a specified box on a specific page of a PDF.

    Parameters:
    - pdf_path: Path to the PDF file.
    - page_number: Page number (starting from 0) from which to extract text.
    - box_coords: Tuple (x0, y0, x1, y1) representing the box coordinates.
    """
    doc = fitz.open(pdf_path)

    # Ensure the specified page number is within valid range
    if 0 <= page_number < doc.page_count:
        page = doc[page_number]

        # Extract text from the specified box
        rect = fitz.Rect(*box_coords)
        #print(rect)
        text = page.get_text("text", clip=rect)

        # Display the extracted text
        print(text)

    doc.close()

pdf_path = 'invoice1.PDF'
field_coordinates={}
# Replace 0 with the desired page number (index starts from 0)
column_list1=["Exporter:","Invoice","Exporter's","Consignee:","NOTIFY","Buyer_Order_No.",
             "Other_Exporter_Details:","Buyer_(if_other","Country_of_Origin","Country_of_Final"]
#column_list1=["Country_of_Origin","Country_of_Final"]
page_number = 0
doc = fitz.open(pdf_path)
page = doc[page_number]
text = page.get_text("words")
for column in column_list1:
    if('_' not in column):
      for word in text:
         if (column == word[4]):
             field_coordinates[column+'_x0']=word[0]
             field_coordinates[column +'_y0'] = word[1]
             field_coordinates[column + '_x1'] = word[2]
             field_coordinates[column +'_y1'] = word[3]
    if ('_' in column):
      word_search = []
      column_split=column.split('_')
      list1=[]
      list2=[]
      list3=[]
      #print(column_split)
      for word in text:
          if (column_split[0]==word[4]):
             list1.append(word)
          if (column_split[1] == word[4]):
            list2.append(word)
          if (column_split[2]==word[4]):
             list3.append(word)
      i=0
      while(i<len(list1)):
          j=0
          while(j<len(list2)):
              k=0
              while(k<len(list3)):
                #print(list1[i][4],list2[j][4],list3[k][4],column)
                if (list1[i][5]==list2[j][5] and list1[i][5]==list2[j][5] and column_split[0]==list1[i][4] and
                        column_split[1]==list2[j][4] and column_split[2]==list3[k][4] and
                         list1[i][7]+1==list2[j][7] and list2[j][7]+1==list3[k][7] and list1[i][6]==list2[j][6] and list1[i][6]==list3[k][6]):
                   #print(list1[i][6],list2[j][6],list3[k][6])
                   pos=i
                else:
                    pass
                k=k+1
              j=j+1
          i=i+1
      field_coordinates[column + '_x0'] = list1[pos][0]
      field_coordinates[column + '_y0'] = list1[pos][1]
      field_coordinates[column + '_x1'] = list1[pos][2]
      field_coordinates[column + '_y1'] = list1[pos][3]


doc.close()
#print(field_coordinates)
#print(list3)
closer_dict={"Exporter:":"Other_Exporter_Details:","Invoice":"Exporter's","Exporter's":"Exporter's",
             "Buyer_Order_No.":"Other_Exporter_Details:","Other_Exporter_Details:":"Buyer_(if_other",
             "Consignee:":"Buyer_(if_other","NOTIFY":"Country_of_Origin","Country_of_Origin":"Country_of_Final",
             "Country_of_Final":"Country_of_Final"}
#closer_dict={"Exporter's":"Exporter's"}
#column_list_test=["Exporter:","Invoice","Exporter's","Buyer_Order_No.","Other_Exporter_Details:",
 #                 "Consignee:","NOTIFY","Country_of_Origin"]
#column_list_test=["Exporter's"]
#print(field_coordinates)
#column_list_test=["Country_of_Origin","Country_of_Final"]
column_list_test=column_list1
for column in column_list_test:
    x0=field_coordinates[column+'_x0']
    y0=field_coordinates[column+'_y0']
    closer_column=closer_dict[column]
    #print(column,x0,y0)
    #print(column)
    if column=='Invoice':
     x1 = field_coordinates[closer_column + '_x0']
     y1 = field_coordinates[closer_column + '_y0']+15
    elif column=="Exporter's":
        x1=500
        y1=field_coordinates[column+'_y0']+15
    elif column=="Buyer_Order_No.":
        x1=500
        y1=field_coordinates[closer_column + '_y1']
    elif column=="Other_Exporter_Details:":
        x1=500
        y1=field_coordinates[closer_column + '_y1']-10
    elif column=="Consignee:":
        x1=field_coordinates[closer_column + '_x0']
        y1=field_coordinates[closer_column + '_y0']+40
    elif column=="Country_of_Origin":
        x1=field_coordinates[closer_column + '_x0']
        y1=field_coordinates[closer_column + '_y0']+20
    elif column=="Country_of_Final":
        x1=500
        y1=field_coordinates[column + '_y0']+20
    else:
        x1 = field_coordinates[closer_column + '_x0']
        y1 = field_coordinates[closer_column + '_y0']
    #print(x1)
    box_coords=(x0,y0,x1,y1)
    extract_box_content(pdf_path, page_number, box_coords)
    #print(box_coords)

#extract_box_content(pdf_path, page_number, box_coords)
#with pdfplumber.open("invoice1.PDF") as pdf:
#    first_page = pdf.pages[0]
#    print(first_page.extract_text())
        #x0=rect["x0"]
        #y0 = rect["y0"]
        #x1 = rect["x1"]
        #y1 = rect["y1"]
        #test=(x0,y0,x1,y1)
        #extract_box_content(pdf_path, page_number, test)
        #print("box seprator")




