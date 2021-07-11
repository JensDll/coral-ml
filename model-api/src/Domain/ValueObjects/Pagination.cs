using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.ValueObjects
{
    public record Pagination(int PageNumber, int PageSize)
    {
        public (int skip, int take) GetSkipTake()
        {
            int skip = PageNumber * PageSize - PageSize;
            int take = PageSize;

            return (skip, take);
        }
    }
}
