using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.DataTransfer
{
    public class PaginationEnvelope<T>
    { 
        public IEnumerable<T> Data { get; set; }

        public int PageNumber { get; set; }

        public int PageSize { get; set; }

        public int Total { get; set; }
    }
}
