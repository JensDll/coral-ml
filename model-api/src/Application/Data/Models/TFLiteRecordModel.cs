using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Models
{
    public class TFLiteRecordModel
    {
        public int Id { get; set; }

        public string ModelName { get; set; }

        public byte[] ZipContent { get; set; }

        public bool Loaded { get; set; }
    }
}
