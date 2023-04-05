# -*- coding: utf-8 -*-
import pypdfannot.utils as utils
import fitz
import re
import os


class Note_extractor():
    def __init__(self,file: str):
        self.file = file
        self.pdf = fitz.open(self.file)

    def notes_extract(self):
        self.highlights = list()
        for page_num in range(0,self.pdf.page_count-1):
            page = self.pdf[page_num]
            page_bound = list(page.bound())
            # print(page_bound)
            for annot in page.annots():
                margin = (-2, -2, 2, 2)
                anotacao = {}
                anotacao["type"] = annot.type[1]
                anotacao["page"] = page_num + 1
                anotacao["author"] = annot.info["title"]
                anotacao["author"] = annot.info["title"]
                anotacao["rect_coord"] = list(annot.rect)
                # Adjust by page size
                anotacao["rect_coord"][0] = anotacao["rect_coord"][0]/page_bound[2]
                anotacao["rect_coord"][1] = anotacao["rect_coord"][1]/page_bound[3]
                anotacao["rect_coord"][2] = anotacao["rect_coord"][2]/page_bound[2]
                anotacao["rect_coord"][3] = anotacao["rect_coord"][3]/page_bound[3]
                # print(annot.type[1])
                anotacao["start_xy"] = anotacao["rect_coord"][0:2]
                text = ''
                margin_h = 3
                margin_w = 3
                if annot.vertices and len(annot.vertices) >= 4 and not annot.type[1] in ["Ink","Freetext"]:
                    vertices = annot.vertices
                    for i in range(0,len(vertices),4):
                        range_interval = slice(i,i+4)
                        rect = vertices[range_interval]
                        clip = fitz.Rect(rect[0],rect[3])
                        subtext = page.get_text(clip = clip)
                        text = text + subtext
                        while(subtext == ''):
                            margin_w = margin_w +1
                            x0 = rect[0][0] - margin_w
                            y0  = rect[0][1] - margin_w
                            x1 = rect[3][0] + margin_w
                            y1  = rect[3][1] + margin_w
                            clip = fitz.Rect(x0,y0,x1,y1)
                            # print(clip)
                            subtext = page.get_text(clip = clip)
                            text = text + subtext
                            if margin_w >= 50:
                                break

                anotacao["text"] = text
                anotacao['content'] = annot.info['content']
                anotacao["created"] = annot.info["creationDate"]
                anotacao["color_name"] = list(annot.colors["stroke"])
                self.highlights.append(anotacao)

    def adjust_date(self):
        """
        Converts the created date to the format YYYY-MM-DD HH:mm:ss
        """
        for annot in self.highlights:
            date_created = re.sub("D:","",annot["created"])
            # Extract Date in format: YYYY-MM-DD HH:MM:SS
            regex_pattern_date = "([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*"
            regex_export_date = r"\1-\2-\3 \4:\5:\6"
            date_created = re.sub(regex_pattern_date,regex_export_date,date_created)
            annot["created"] = date_created

    def adjust_color(self):
        """
        Converts the RGB color to classified group. This method converts RGB to HSL and convert HSL to categorical
        color names. The default color é Yellow
        """
        for annot in self.highlights:
            color = annot["color_name"]
            color_hls = utils.convert_to_hls(color)
            color_names = utils.colors_names(color_hls)
            annot["color_name"] = color_names

    def adjust_text(self):
        """
        Adjust text with hifenization and remove all the linebreaks from content.
        """
        for annot in self.highlights:
            text = annot["content"]
            text = utils.cleanup_text(text)
            text = utils.merge_lines(captured_text=text,remove_hyphens=True)
            annot["content"] = text

    def extract_image(self,location:str, folder = "img/"):
        for annot in self.highlights:
            if 'annot_number' not in locals():
                annot_number = 0
            if annot['type'] == 'Square':
                annot_number = annot_number + 1
                page = annot['page'] - 1


                pdf_page = self.pdf[page]

                # Remove annotations in the page
                try:
                    for annots in pdf_page.annots():
                        pdf_page.delete_annot(annots)
                except:
                    pass
                user_space = annot["rect_coord"]
                # area = pdf_page.get_pixmap(dpi = 300)
                area = pdf_page.bound()
                # area = user_space
                area.x0 = user_space[0]*area[2]
                area.x1 = user_space[2]*area[2]
                area.y0 = user_space[1]*area[3]
                area.y1 = user_space[3]*area[3]

               

                clip = fitz.Rect(area.tl, area.br)

                # print(clip)

                if not os.path.exists(location):
                    os.mkdir(location)
                if not os.path.exists(location+"//"+folder):
                    os.mkdir(location+"/"+folder)

                file = re.sub("(.*/|.*\\\\)","",self.file)
                file = re.sub("[.]pdf","",file)
                page = page +1

                file_name = file+"_p"+str(page)+'_'+str(annot_number) + ".png"

                file_export = location+"/"+folder+file_name
                # file_export = os.path.dirname(file_export)


                # print(pdf_page,' - annotation number: ', annot_number)

                img_folder = folder +  "/" +file_name
                img_folder = re.sub("/+","/",img_folder)

                img = pdf_page.get_pixmap(clip = clip,dpi = 300)
                print(file_export)
                img.save(file_export)

                if os.path.exists(file_export):
                    annot['has_img'] = True
                    annot['img_path'] = img_folder
                else:
                    annot['has_img'] = False
                    annot['img_path'] = ""
            self.reload()

    def reorder_custom(self,criteria = ['page',"start_xy"], ordenation = 'asc'):
        self.highlights = utils.annots_reorder_custom(self.highlights,criteria=criteria,ordenation=ordenation)

    def reorder_columns(self,columns = 1, tolerance = 0.1):
        self.highlights = utils.annots_reorder_columns(self.highlights,columns=columns, tolerance=tolerance)

    def reload(self):
        self.close()
        self.pdf = fitz.open(self.file)

    def extract_ink(self,location:str, folder = "img/"):
        list_pages = dict()
        for annot in self.highlights:
            if annot['type'] == 'Ink':
                if 'anterior_page' not in locals():
                    anterior_page = annot["page"]
                    anterior_userspace = annot["rect_coord"]
                    anterior = 1
                    anterior_number = 1
                page_number = annot["page"]
                page = annot['page'] - 1

                pdf_page = self.pdf[page]

                # print(page_number)

                # Remove annotations in the page
                try:
                    for annots in pdf_page.annots():
                        if annots.type[1] != "Ink":
                            pdf_page.delete_annot(annots)
                except:
                    print("No annotations to exclude")


                user_space = annot["rect_coord"]
                # area = pdf_page.get_pixmap(dpi = 300)
                area = pdf_page.bound()
                page_area = pdf_page.bound()
                # area = user_space
                if page_number == anterior_page:
                    anterior += 1
                    area.x0 = min(user_space[0],anterior_userspace[0]) * area[2]
                    area.x1 = max(user_space[2],anterior_userspace[2]) * area[2]
                    area.y0 =  min(user_space[1],anterior_userspace[1]) * area[3]
                    area.y1 =  max(user_space[3],anterior_userspace[3]) * area[3]
                else:
                    anterior = 1
                    area.x0 = user_space[0] * area[2]
                    area.x1 = user_space[2] * area[2]
                    area.y0 = user_space[1] * area[3]
                    area.y1 = user_space[3] * area[3]

               

                clip = fitz.Rect(area.tl, area.br)
                page_numeration = 'p_' + str(page+1)

                file = re.sub(".*/","",self.file)
                file = re.sub("[.]pdf","",file)
                page = page +1

                file_name = file+"_p"+str(page)+'_ink' + ".png"

                file_export = location+"/"+folder+file_name
                file_export = re.sub("/+","/",file_export)


                # print(pdf_page,' - annotation number: ', annot_number)

                img_folder = folder +  "/" +file_name
                img_folder = re.sub("/+","/",img_folder)

                list_pages[page_numeration] = {"page": page,"clip": clip,"file": file, "file_name": file_name, "file_export": file_export}

                anterior_page = annot["page"]
                anterior_userspace = [clip.x0/page_area[2],clip.y0/page_area[3],clip.x1/page_area[2],clip.y1/page_area[3]]
                anterior_number = anterior


        # print(list_pages)
        for pg in list_pages:
            if not os.path.exists(location):
                os.mkdir(location)
            if not os.path.exists(location+"/"+folder):
                os.mkdir(location+"/"+folder)


            pdf_page = self.pdf[list_pages[pg]["page"]]
            

            img = pdf_page.get_pixmap(clip = list_pages[pg]["clip"],dpi = 300)
            # print(file_export)
            # if anterior <= anterior_number:
            img.save(list_pages[pg]["file_export"])

            if os.path.exists(file_export):
                annot['has_img'] = True
                annot['img_path'] = img_folder
            else:
                annot['has_img'] = False
                annot['img_path'] = ""

        for annot in self.highlights[:]:
            if annot["type"] == "Ink" and not "has_img" in annot:
                # print(annot)
                self.highlights.remove(annot)
        self.reload()

    def close(self):
        self.pdf.close()
    

