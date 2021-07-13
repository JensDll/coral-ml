using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.DataTransfer.Record
{
    public class RecordCreate
    {
        public string ModelFileName { get; set; }

        public string LabelFileName { get; set; }

        public byte[] ZipContent { get; set; }

        public int RecordTypeId { get; set; }
    }
}
