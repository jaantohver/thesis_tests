using System;
using System.IO;
using System.Drawing.Imaging;
using System.Collections.Generic;
using System.Text.RegularExpressions;

using iTextSharp.text;
using iTextSharp.text.pdf;
using iTextSharp.text.pdf.parser;

using Ghostscript.NET.Rasterizer;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace pdf_utils
{
    class MainClass
    {
        const string outputFolder = @"/Users/jaan/Projects/kool/";

        public static void Main(string[] args)
        {
            //ConvertTextToPDF();

            Test().Wait();

            //if (Environment.Is64BitProcess)
            //{
            //    PdfToPng("../../test.pdf", "../../test");
            //}
        }

        static async Task Test()
        {
            //Create an instance of our strategy
            var strat = new MyLocationTextExtractionStrategy();

            PdfReader reader = new PdfReader("../../test.pdf");
            int numPages = reader.NumberOfPages;
            reader.Close();
            reader.Dispose();

            int chunkCount = 5;
            List<List<int>> chunks = new List<List<int>>();

            int start = 0;
            int end = 0;

            for (int i = 0; i < chunkCount; i++)
            {
                start = end + 1;
                end = start + (numPages / chunkCount);
                if (end > numPages || i == chunkCount - 1)
                {
                    end = numPages;
                }

                chunks.Add(Enumerable.Range(start, end).ToList());
            }

            List<Task> tasks = new List<Task>();

            for (int i = 0; i < chunkCount; i++)
            {
                //object arg = i;
                //Task t = new Task(new Action<object>((index) =>
                //{
                using (var r = new PdfReader("../../test.pdf"))
                {
                    //r.SelectPages(chunks[(int)index]);
                    r.SelectPages(chunks[i]);

                    for (int j = 1; j < r.NumberOfPages; j++)
                    {
                        Console.WriteLine("Extracting text from page {0}", j);
                        string ex = PdfTextExtractor.GetTextFromPage(r, j, strat);
                    }

                    r.Close();
                }
                //}), arg);
                //tasks.Add(t);
                //t.Start();
            }

            //await Task.WhenAll(tasks);

            //Loop through each chunk found
            foreach (var p in strat.myPoints)
            {
                Console.WriteLine(string.Format("Found text {0} at (x:{1}, y:{2}, w:{3}, h:{4})",
                    p.Text, p.Rect.Left, p.Rect.Top, p.Rect.Width, p.Rect.Height));
            }
        }

        static void ConvertTextToPDF()
        {
            StreamReader reader = new StreamReader("../../test.txt");
            Document doc = new Document();
            doc.AddDocListener(new DocListener());
            PdfWriter.GetInstance(doc, new FileStream("../../test.pdf", FileMode.Create));
            doc.Open();

            int counter = 0;

            while (reader.Peek() >= 0)
            {
                string content = reader.ReadLine();
                content = content.Trim();

                if (!string.IsNullOrWhiteSpace(content))
                {
                    var matches = Regex.Matches(content, @"\b[\w']*\b");

                    foreach (Match m in matches)
                    {
                        if (!string.IsNullOrWhiteSpace(m.Value) && !int.TryParse(m.Value, out _))
                        {
                            doc.Add(new Paragraph(m.Value));
                            counter++;
                        }

                        if (counter == 30)
                        {
                            counter = 0;
                            doc.NewPage();
                        }
                    }
                }
            }

            doc.Close();
        }

        private static void PdfToPng(string inputFile, string outputFileName)
        {
            var xDpi = 100; //set the x DPI
            var yDpi = 100; //set the y DPI
            var pageNumber = 1; // the pages in a PDF document

            using (var rasterizer = new GhostscriptRasterizer()) //create an instance for GhostscriptRasterizer
            {
                rasterizer.Open(inputFile); //opens the PDF file for rasterizing

                //set the output image(png's) complete path
                var outputPNGPath = System.IO.Path.Combine(outputFolder, string.Format("{0}.png", outputFileName));

                //converts the PDF pages to png's 
                var pdf2PNG = rasterizer.GetPage(xDpi, yDpi, pageNumber);

                //save the png's
                pdf2PNG.Save(outputPNGPath, ImageFormat.Png);

                Console.WriteLine("Saved " + outputPNGPath);
            }
        }
    }

    public class MyLocationTextExtractionStrategy : LocationTextExtractionStrategy
    {
        //Hold each coordinate
        public List<RectAndText> myPoints = new List<RectAndText>();

        //Automatically called for each chunk of text in the PDF
        public override void RenderText(TextRenderInfo renderInfo)
        {
            base.RenderText(renderInfo);

            //Get the bounding box for the chunk of text
            var bottomLeft = renderInfo.GetDescentLine().GetStartPoint();
            var topRight = renderInfo.GetAscentLine().GetEndPoint();

            //Create a rectangle from it
            var rect = new Rectangle(bottomLeft[Vector.I1], bottomLeft[Vector.I2], topRight[Vector.I1], topRight[Vector.I2]);

            if (!string.IsNullOrWhiteSpace(renderInfo.GetText()))
            {
                //Add this to our main collection
                myPoints.Add(new RectAndText(rect, renderInfo.GetText()));
            }
        }
    }

    //Helper class that stores our rectangle and text
    public class RectAndText
    {
        public Rectangle Rect;
        public string Text;
        public RectAndText(Rectangle rect, string text)
        {
            Rect = rect;
            Text = text;
        }
    }

    public class DocListener : IDocListener
    {
        public int PageCount { get; set; }

        public bool Add(IElement element)
        {
            return true;
        }

        public void Close()
        {
        }

        public void Dispose()
        {
        }

        public bool NewPage()
        {
            PageCount++;

            return true;
        }

        public void Open()
        {
        }

        public void ResetPageCount()
        {
        }

        public bool SetMarginMirroring(bool marginMirroring)
        {
            return true;
        }

        public bool SetMarginMirroringTopBottom(bool marginMirroringTopBottom)
        {
            return true;
        }

        public bool SetMargins(float marginLeft, float marginRight, float marginTop, float marginBottom)
        {
            return true;
        }

        public bool SetPageSize(Rectangle pageSize)
        {
            return true;
        }
    }
}