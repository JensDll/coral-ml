using Application.Data.Services;
using Contracts.Request;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Infrastructure.Data.Services
{
    public class PaginationService : IPaginationService
    {
        public (int skip, int take) SkipTake(PaginationRequestDto request)
        {
            int skip = request.PageNumber * request.PageSize - request.PageSize;
            int take = request.PageSize;

            return (skip, take);
        }
    }
}
