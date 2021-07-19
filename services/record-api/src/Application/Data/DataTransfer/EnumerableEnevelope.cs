using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.DataTransfer
{
    public class EnumerableEnevelope<T>
    {
        public IEnumerable<T> Data { get; init; }

        public int Total => Data.Count();
    }
}
